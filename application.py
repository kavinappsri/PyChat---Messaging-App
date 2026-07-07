from client import Client
from gui.mainWindow import MainWindow
from jsonDB import jsonDB
from config.defaults import CONFIG_DEFAULT
from PySide6.QtWidgets import QApplication


class Application:
    def __init__(self, qtApp: QApplication):
        self.qtApp = qtApp
        self.config = jsonDB("config.json", CONFIG_DEFAULT)
        self.client = Client(self.config)
        self.mainWindow = MainWindow()
        
        self.mainWindow.connectPage.connectionRequested.connect(self.client.tryConnect)
        self.mainWindow.chatPage.disconnectRequested.connect(self.client.disconnectFromServer)
        self.mainWindow.chatPage.messageSendRequested.connect(self.client.sendMessage)
        self.client.connected.connect(self.mainWindow.showChatPage)
        self.client.messageReceived.connect(self.mainWindow.chatPage.addMessage)
        self.client.disconnected.connect(self.mainWindow.showConnectPage)
        self.client.connectionError.connect(lambda e: print(e))
        
    def run(self):
        self.mainWindow.show()
        self.qtApp.exec()