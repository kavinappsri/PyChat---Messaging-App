from PySide6.QtCore import QObject, Signal, Slot
from network import socketClientManager


class Client(QObject):
    connected = Signal()
    disconnected = Signal()
    connectionError = Signal(str)
    messageReceived = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.socketClient = None
        self.receiveThread = None
        self.stopEvent = None
   
    @Slot(str, int)     
    def tryConnect(self, ip: str, port:int) -> None:
        
        username = "guest"
        password = "12345"
        
        self.socketClient = socketClientManager("utf-8")
        
        try:
            self.socketClient.connect(ip, port)
        except Exception as e:
            self.connectionError.emit(str(e))
            
        
    
    def disconnectFromServer(self):
        self.socketClient.close()
    
    def sendMessage(self, message):
        pass
    


    