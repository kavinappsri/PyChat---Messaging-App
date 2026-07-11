from pathlib import Path
from threading import Thread
from json import loads, dumps

from network import socketServerManager
from jsonDB import jsonDB
from server.userInt import userInt
from server.const import *

        
class Server:
    def __init__(self):
        configPath = Path(__file__).parent / "serverconfig.json"
        
        self.terminal: userInt = userInt('')
        self.config: jsonDB = jsonDB(configPath, CONFIG_DEFAULT)
        self.server: socketServerManager = socketServerManager(self.config.data['ip'], self.config.data['port'])
        self.serverThread =  Thread(target=self.server.start, daemon=True)
        self.inputThread = Thread(target=self._inputThread, daemon=True)
        
    def _inputThread(self):
        while True:
            cmd = self.terminal.getInput()
            if cmd == self.config.data["stopWord"]:
                self.terminal.print("[SHUTDOWN THREAD] Commencing Shutdown Process")
                self.server.stop()
                break
        
    def run(self) -> None:
        self.serverThread.start()
        self.inputThread.start()
        
        self.terminal.print(f"[SERVER] Server started on {self.config.data['ip']}:{self.config.data['port']}")
        self.terminal.print(f"[SERVER] Server name: {self.config.data['serverName']}")
        
        while True:
            packet = self.server.inputQueue.get()
            
            if packet is None:
                break
            
            try:
                data = loads(packet[1])
            except:
                self.server.send(packet[0], dumps(BAD_REQUEST_RESPONSE))
                continue 
                
            if "action" not in data:
                self.server.send(packet[0], dumps(BAD_REQUEST_RESPONSE))
                continue

            elif data["action"] == "register":
                self.terminal.print(f"[SERVER] Register request | Client ID: {packet[0]}")
    
                if "username" not in data or "password" not in data:
                    self.server.send(packet[0], dumps(BAD_REQUEST_RESPONSE))
                    continue
                elif data["username"] in  self.config.data["registeredClients"]:
                    self.server.send(packet[0], dumps(ACTION_DENIED_RESPONSE))
                    continue
                else:
                    self.config.data["registeredClients"][data["username"]] = data["password"]
                    self.config.save()
                    self.server.send(packet[0], dumps(OK_RESPONSE))
                    self.terminal.print(f"[SERVER] Registered client | Username: {data['username']}")
                    continue

            elif data["action"] == "msg":
                self.terminal.print(f"[SERVER] Message request | Client ID: {packet[0]}")
            
                if "username" not in data or "password" not in data or "message" not in data:
                    self.server.send(packet[0], dumps(BAD_REQUEST_RESPONSE))
                    continue
                elif data["username"] not in  self.config.data["registeredClients"]:
                    self.server.send(packet[0], dumps(ACTION_DENIED_RESPONSE))
                    continue
                elif data["password"] != self.config.data["registeredClients"][data["username"]]:
                    self.server.send(packet[0], dumps(ACTION_DENIED_RESPONSE))
                    continue
                else:
                    if not data["message"].strip():
                        self.server.send(packet[0], dumps(OK_RESPONSE))
                        continue
            
                    sendable = {
                        "status":"1",
                        "ping":data["message"],
                        "author":data["username"]
                    }
                    self.server.sendallQueue.put(dumps(sendable))

                    self.terminal.print(f"[SERVER] Message sent | Username: {data['username']} | Message: {data['message']}")

            elif data["action"] == "getName":
                if "username" not in data or "password" not in data:
                    self.server.send(packet[0], dumps(BAD_REQUEST_RESPONSE))
                    continue
                elif data["username"] not in  self.config.data["registeredClients"]:
                    self.server.send(packet[0], dumps(ACTION_DENIED_RESPONSE))
                    continue
                elif data["password"] != self.config.data["registeredClients"][data["username"]]:
                    self.server.send(packet[0], dumps(ACTION_DENIED_RESPONSE))
                    continue
                else:
                    sendable = {
                        "status":"1",
                        "name":self.config.data["serverName"]
                    }
                    self.server.send(packet[0], dumps(sendable))
        
            #Invalid Action
            else:
                self.server.send(packet[0], dumps(BAD_REQUEST_RESPONSE))
                
