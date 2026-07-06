from client import Client
from gui.mainWindow import MainWindow
from PySide6.QtWidgets import QApplication


class Application:
    def __init__(self, qtApp: QApplication):
        self.qtApp = qtApp
        self.client = Client()
        self.mainWindow = MainWindow()
        
        self.mainWindow.connectPage.connectionRequested.connect(self.client.tryConnect)
        self.client.connected.connect(self.mainWindow.showChatPage)
        self.client.connectionError.connect(lambda e: print(e))
        
    def run(self):
        self.mainWindow.show()
        self.qtApp.exec()