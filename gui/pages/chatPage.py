from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont

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
        self.devPlaceholder = QLabel("Message Area (Coming Soon !!!)")
        self.messageEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.disconnectButton = QPushButton("Disconnect")
        
        self.messageEdit.setPlaceholderText("Type a message...")
        
        
        
    def _createLayout(self):
        self.layout = QVBoxLayout()
        self.inputBar = QHBoxLayout()
        self.topBar = QHBoxLayout()
        
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)

        self.inputBar.addWidget(self.messageEdit)
        self.inputBar.addWidget(self.sendButton)
        
        self.topBar.addWidget(self.serverLabel)
        self.topBar.addStretch()
        self.topBar.addWidget(self.disconnectButton)
        
        self.layout.addLayout(self.topBar)
        self.layout.addStretch()
        self.layout.addWidget(self.devPlaceholder)
        self.layout.addStretch()
        self.layout.addLayout(self.inputBar)
        
        
        
    def _applyStyles(self):
        self.serverLabel.setFont(QFont("Arial", 20))
        self.devPlaceholder.setFont(QFont("Arial", 12))
        
    def _trySendMessage(self):
        if not self.messageEdit.text().strip():
            return
        
        self.messageSendRequested.emit(self.messageEdit.text())
        self.messageEdit.clear()
        
        