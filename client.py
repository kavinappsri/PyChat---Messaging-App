import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal
from gui.mainWindow import MainWindow


class Client(QObject):
    connected = Signal()
    disconnected = Signal()
    connectionFailed = Signal(str)
    messageReceived = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.socketClient = None
        self.receiveThread = None
        self.stopEvent = None
        
    def tryConnect(self):
        pass
    
    def disconnect(self):
        pass
    
    def sendMessage(self, message):
        pass
    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
    
if __name__ == "__main__":
    main()
    