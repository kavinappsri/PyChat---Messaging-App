from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont

class ChatPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self._createWidgets()
        self._createLayout()
        self._applyStyles()
        
        self.setLayout(self.layout)       
        
    def _createWidgets(self):
        self.title = QLabel("Chat Room (Coming soon)")
        
    def _createLayout(self):
        self.layout = QVBoxLayout()
        
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        
    def _applyStyles(self):
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title.setFont(QFont("Arial", 26))
        
        