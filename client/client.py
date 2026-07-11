from threading import Thread, Event
from PySide6.QtCore import QObject, QThread, Signal, Slot
from network import socketClientManager
import json


class ConnectionWorker(QObject):
    
    finished = Signal()
    
    def __init__(self, client: Client, ip: str, port: int):
        super().__init__()
        self.client: Client = client
        self.ip: str = ip
        self.port: int = port
        
    @Slot()
    def run(self):
        try:
            self.client._tryConnect(self.ip, self.port)
        finally:
            self.finished.emit()

class Client(QObject):
    connected = Signal(str)
    disconnected = Signal()
    connectionError = Signal(str)
    messageReceived = Signal(str, bool, str)
    
    def __init__(self, config):
        super().__init__()
        self.socketClient: socketClientManager | None = None
        self.receiveThread: Thread | None = None
        self.stopEvent: Event| None = None
        self.config = config
        self.currentConnectedServerIp: str | None = None
        self.currentConnectedServerPort: int | None = None
        self.connectionWorker: ConnectionWorker | None = None
        self.connectionThread: QThread | None = None
        self.currentlyConnecting: bool = False
        self.currentServerName: str | None = None
      
    def _tryConnect(self, ip: str, port: int) -> None:
        
        encoding = self.config.data["encoding"]
        self.currentConnectedServerIp = ip
        self.currentConnectedServerPort = port
        self.currentlyConnecting = True

        self.socketClient = socketClientManager(encoding)
        try:
            assert self.socketClient is not None
            
            self.socketClient.connect(ip, port)
            
            self._registerServer()
            self._registerInServer()
            self._getServerDetails()
            
            self.stopEvent = Event()
            recvThread = Thread(target=self._receiveThread, daemon=True)
            recvThread.start()
            
            self.connected.emit(self.currentServerName)
            
        except Exception as e:
            self.connectionError.emit(str(e))
            self.currentConnectedServerIp = None
            self.currentConnectedServerPort = None
            self.currentlyConnecting = False
            
        
    @Slot()
    def disconnectFromServer(self) -> None:
        '''disconnects from the server'''
        if self.socketClient is not None:
            
            self.stopEvent.set()
            self.socketClient.close()

            self.currentConnectedServerIp = None
            self.currentConnectedServerPort = None
            self.currentlyConnecting = False
            
            self.disconnected.emit()
    
    @Slot(str)
    def sendMessage(self, message: str) -> None:
        '''Sends a message to the server'''
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
            self.currentlyConnecting = False
    
    def _registerServer(self):
        if self.currentConnectedServerIp not in self.config.data["servers"]:
            
            self.config.data["servers"][self.currentConnectedServerIp] = {
                "ip": self.currentConnectedServerIp,
                "port": self.currentConnectedServerPort,
                "registered": False
            }
            self.config.save()
            
    def _registerInServer(self):
        assert self.socketClient is not None
        
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
            
    def _getServerDetails(self):
        assert self.socketClient is not None
        
        detailRequestData = {
            "action":"getName",
            "username":self.config.data["username"],
            "password":self.config.data["password"]
        }
        
        self.socketClient.send(json.dumps(detailRequestData))
        response = json.loads(self.socketClient.tryRecv())
        
        if "status" not in response:
            raise Exception("Invalid server response")
        elif response["status"] != "1":
            raise Exception(f"Server responded with status {response['status']}, error: {response['Error']}")
        elif "name" not in response:
            raise Exception("Invalid server response")
    
        
        self.currentServerName = response["name"]
            
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
                    if "ping" in data and "author" in data:
                        isUser = data['author'] == self.config.data["username"]
                        self.messageReceived.emit(data['ping'], isUser, data['author']) 
                        
        except Exception as e:
            if not self.stopEvent.is_set():
                self.connectionError.emit(str(e))
                
    @Slot(str, int)
    def connectAsync(self, ip: str, port: int) -> None:
        '''Instatiates a thread that establishes a connection to the server'''
        if self.currentlyConnecting:
            return
        
        self.connectionWorker = ConnectionWorker(self, ip, port)
        self.connectionThread = QThread()
        
        assert self.connectionWorker is not None
        assert self.connectionThread is not None
        
        self.connectionWorker.moveToThread(self.connectionThread)
        self.connectionThread.started.connect(self.connectionWorker.run)
        self.connectionWorker.finished.connect(self.connectionThread.quit)
        self.connectionThread.finished.connect(self.connectionThread.deleteLater)
        self.connectionWorker.finished.connect(self.connectionWorker.deleteLater)
        
        
        self.connectionThread.start()
        
                    
            
            
    


    