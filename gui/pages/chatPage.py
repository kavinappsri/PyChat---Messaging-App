from PySide6.QtCore import Signal, Slot, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QFont
from gui.widgets.messageBubble import MessageBubble

class ChatPage(QWidget):
    
    messageSendRequested = Signal(str)
    disconnectRequested = Signal()
    
    def __init__(self):
        super().__init__()
        
        self._createWidgets()
        self._createLayout()
        self._applyStyles()
        
        self.setLayout(self.layout) 
        
        self.sendButton.clicked.connect(self._trySendMessage)
        self.disconnectButton.clicked.connect(self.disconnectRequested.emit)
        
    def _createWidgets(self):
        self.serverLabel = QLabel("Server Name")
        self.messageScrollArea = QScrollArea()
        self.messageArea = QWidget()
        self.messageScrollArea.setWidgetResizable(True)
        self.messageEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.disconnectButton = QPushButton("Disconnect")
        
        self.messageEdit.setPlaceholderText("Type a message...")
        
        
        
        
    def _createLayout(self):
        self.layout = QVBoxLayout()
        self.scrollLayout = QVBoxLayout()
        self.inputBar = QHBoxLayout()
        self.topBar = QHBoxLayout()
        
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)

        self.inputBar.addWidget(self.messageEdit)
        self.inputBar.addWidget(self.sendButton)
        
        self.topBar.addWidget(self.serverLabel)
        self.topBar.addStretch()
        self.topBar.addWidget(self.disconnectButton)
        
        self.scrollLayout.addStretch()
        
        self.messageArea.setLayout(self.scrollLayout)
        self.messageScrollArea.setWidget(self.messageArea)
        
        self.layout.addLayout(self.topBar)
        self.layout.addWidget(self.messageScrollArea)
        self.layout.addLayout(self.inputBar) 
        
    def _applyStyles(self):
        self.serverLabel.setFont(QFont("Arial", 20))
        self.messageArea.setFont(QFont("Arial", 12))

        self.scrollLayout.setSpacing(5)
        
    def _trySendMessage(self):
        if not self.messageEdit.text().strip():
            return
        
        self.messageSendRequested.emit(self.messageEdit.text())
        self.messageEdit.clear()
        
    @Slot(str, bool, str)
    def addMessage(self, message: str, isUserMessage: bool, author: str) -> None:
        
        rowWidget = QWidget()
        rowLayout = QHBoxLayout()

        rowLayout.setContentsMargins(0, 0, 0, 0)
        rowLayout.setSpacing(0)
        
        
        if isUserMessage:
            rowLayout.addStretch()
            rowLayout.addWidget(MessageBubble(message, isUserMessage, author))
        else:
            rowLayout.addWidget(MessageBubble(message, isUserMessage, author))
            rowLayout.addStretch()
        
        rowWidget.setLayout(rowLayout)
        self.scrollLayout.addWidget(rowWidget)
        QTimer.singleShot(
            1,
            lambda: self.messageScrollArea.verticalScrollBar().setValue(
                self.messageScrollArea.verticalScrollBar().maximum()
            )
        )
        
    def setServerName(self, name: str) -> None:
        self.serverLabel.setText(name)
        
    def clearMessages(self) -> None:
        assert self.messageScrollArea.widget() is not None
        
        self.messageScrollArea.widget().deleteLater()
        
        self.messageArea = QWidget()
        self.scrollLayout = QVBoxLayout()

        self.scrollLayout.addStretch()
        
        self.messageArea.setLayout(self.scrollLayout)
        self.messageScrollArea.setWidget(self.messageArea)
