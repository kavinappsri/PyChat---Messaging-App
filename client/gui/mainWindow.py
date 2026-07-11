from PySide6.QtCore import Slot
from PySide6.QtWidgets import QStackedWidget, QWidget, QVBoxLayout
from pathlib import Path
from client.gui.pages.chatPage import ChatPage
from client.gui.pages.connectPage import ConnectPage
from client.gui.pages.errorPage import ErrorPage
from client.gui.pages.loadingPage import LoadingPage


class MainWindow(QWidget):
    '''Main window of the client'''
    def __init__(self):
        super().__init__()
        
        self.setObjectName("MainWindow")
        
        self.setWindowTitle("PyChat")
        self.resize(900, 600)
        
        self._createWidgets()
        self._createLayout()
        self._applyStyles()
        
        self.stack.setCurrentWidget(self.connectPage)
        
        
        
    def _createWidgets(self):
        self.stack = QStackedWidget()
        
        self.connectPage = ConnectPage()
        self.chatPage = ChatPage()
        self.errorPage = ErrorPage()
        self.loadingPage = LoadingPage()
        
        self.stack.addWidget(self.connectPage)
        self.stack.addWidget(self.chatPage)
        self.stack.addWidget(self.errorPage)
        self.stack.addWidget(self.loadingPage)
        
        
    
    def _createLayout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)
        
    def _applyStyles(self):
        style_path = Path(__file__).parent / "styles" / "dark.qss"
        
        with style_path.open() as file:
            self.setStyleSheet(file.read())
        
    @Slot(str)
    def showChatPage(self, serverName: str):
        self.stack.setCurrentWidget(self.chatPage)
        self.chatPage.setServerName(serverName)
        self.chatPage.clearMessages()
        
    @Slot()
    def showConnectPage(self):
        self.stack.setCurrentWidget(self.connectPage)
        
    @Slot(str)
    def showErrorPage(self, error: str):
        self.stack.setCurrentWidget(self.errorPage)
        self.errorPage.setErrorMessage(error)
        
    @Slot()
    def showLoadingPage(self):
        self.stack.setCurrentWidget(self.loadingPage)
    
    