from threading import Thread, Event
from PySide6.QtCore import QObject, Signal, Slot
from network import socketClientManager
import json


class Client(QObject):
    connected = Signal()
    disconnected = Signal()
    connectionError = Signal(str)
    messageReceived = Signal(str)
    
    def __init__(self, config):
        super().__init__()
        self.socketClient: socketClientManager | None = None
        self.receiveThread: Thread | None = None
        self.stopEvent: Event| None = None
        self.config = config
        self.currentConnectedServerIp: str | None = None
        self.currentConnectedServerPort: int | None = None
   
    @Slot(str, int)     
    def tryConnect(self, ip: str, port: int) -> None:
        
        encoding = self.config.data["encoding"]
        self.currentConnectedServerIp = ip
        self.currentConnectedServerPort = port

        self.socketClient = socketClientManager(encoding)
        try:
            self.socketClient.connect(ip, port)
            
            self._registerServer()
            self._registerInServer()
            
            self.stopEvent = Event()
            recvThread = Thread(target=self._receiveThread, daemon=True)
            recvThread.start()
            
            self.connected.emit()
            
        except Exception as e:
            self.connectionError.emit(str(e))
            self.currentConnectedServerIp = None
            self.currentConnectedServerPort = None
            
        
    @Slot()
    def disconnectFromServer(self) -> None:
        if self.socketClient is not None:
            
            self.stopEvent.set()
            self.socketClient.close()

            self.currentConnectedServerIp = None
            self.currentConnectedServerPort = None
            
            self.disconnected.emit()
    
    @Slot(str)
    def sendMessage(self, message: str) -> None:
        try:
            if not message.strip():
                return
            if self.socketClient is None:
                raise Exception("Socket client not found")
            
            messageRequestData = {
                "action":"msg",
                "username":self.config.data["username"],
                "password":self.config.data["password"],
                "message":message
            }
            self.socketClient.send(json.dumps(messageRequestData))
        except Exception as e:
            self.connectionError.emit(str(e))
    
    def _registerServer(self):
        if self.currentConnectedServerIp not in self.config.data["servers"]:
            
            self.config.data["servers"][self.currentConnectedServerIp] = {
                "ip": self.currentConnectedServerIp,
                "port": self.currentConnectedServerPort,
                "registered": False
            }
            self.config.save()
            
    def _registerInServer(self):
        if self.socketClient is None:
            raise Exception("Socket client not initialized")
        
        if not self.config.data["servers"][self.currentConnectedServerIp]["registered"]:
            
            registerRequestData = {
                "action":"register",
                "username":self.config.data["username"],
                "password":self.config.data["password"]
            }
            self.socketClient.send(json.dumps(registerRequestData))
            
            response = json.loads(self.socketClient.tryRecv())
            
            if response is None:
                raise Exception("Server disconnected")
            elif "status" not in response:
                raise Exception("Invalid server response")
            
            elif response["status"] == "1":
                self.config.data["servers"][self.currentConnectedServerIp]["registered"] = True
                self.config.save()
            
            #Checking for already registered server
            elif response["status"] == "3":
                messageRequestData = {
                    "action":"msg",
                    "username":self.config.data["username"],
                    "password":self.config.data["password"],
                    "message":""
                }
                
                self.socketClient.send(json.dumps(messageRequestData))
                response = json.loads(self.socketClient.tryRecv())
                
                if "status" not in response:
                    raise Exception("Invalid server response")
                elif response["status"] != "1":
                    raise Exception(f"Server responded with status {response['status']}, error: {response['Error']}")
                
                self.config.data["servers"][self.currentConnectedServerIp]["registered"] = True
                self.config.save()
            
            else:
                raise Exception(f"Server responded with status {response['status']}, error: {response['Error']}")
            
    def _receiveThread(self):
        try:
            while not self.stopEvent.is_set():
                
                assert self.socketClient is not None, "Socket client not found"
            
                rawData = self.socketClient.tryRecv()
            
                if rawData is None:
                    raise Exception("Server disconnected")
                
                data = json.loads(rawData)
            
                if "status" not in data:
                    raise Exception("Invalid server response")
                elif data['status'] != '1':
                    raise Exception(f"Server responded with status {data['status']}, error: {data['Error']}")
                else:
                    if "ping" in data:
                        self.messageReceived.emit(data['ping']) 
                        
        except Exception as e:
            if not self.stopEvent.is_set():
                self.connectionError.emit(str(e))
                    
            
            
    


    