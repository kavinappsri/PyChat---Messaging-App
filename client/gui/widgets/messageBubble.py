from PySide6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy, QFrame, QHBoxLayout


class MessageBubble(QFrame):
    def __init__(self, text:str, isUser:bool, author:str):
        super().__init__()
        self.text: str = text
        self.isUser: bool = isUser
        self.author: str = author
        
        self._addWidgets()
        self._createLayout()
        self._applyStyles()
        
        
        self.setLayout(self.layout)
        
        if isUser:
            self.textLabel.setObjectName("UserMessage")
        else:
            self.textLabel.setObjectName("OtherMessage")
            
    def _addWidgets(self):
        self.textLabel = QLabel(self.text)
        self.authorLabel = QLabel(self.author)
        
    def _createLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.authorLabel)
        self.layout.addWidget(self.textLabel)
        
    def _applyStyles(self):
        self.textLabel.setMaximumWidth(700)
        self.textLabel.setWordWrap(True)
        self.textLabel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        self.layout.setContentsMargins(0, 0, 0, 0)
        
        