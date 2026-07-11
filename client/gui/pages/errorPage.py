from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame

class ErrorPage(QWidget):
    
    errorPageExit = Signal()
    
    def __init__(self):
        super().__init__()
        
        self._createWidgets()
        self._createLayout()
        self._applyStyles()
        
        self.setLayout(self.layout)
        
        self.okButton.clicked.connect(self.errorPageExit.emit)
        
    def _createWidgets(self):
        self.title = QLabel("Oops! We've hit an error!")
        self.errorLabel = QLabel()
        self.okButton = QPushButton("OK")
        
    def _createLayout(self):
        self.layout = QVBoxLayout()
        self.errorFrame = QFrame()
        self.errorFrameLayout = QVBoxLayout(self.errorFrame)
        
        self.errorFrame.setObjectName("errorFrame")
        
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.layout.addStretch()
        self.errorFrameLayout.addWidget(self.title)
        self.errorFrameLayout.addWidget(self.errorLabel)
        self.layout.addWidget(self.errorFrame)
        self.layout.addStretch()
        self.layout.addWidget(self.okButton)
        
    def _applyStyles(self):
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title.setFont(QFont("Arial", 22))
        self.errorLabel.setFont(QFont("Arial", 15))
        self.title.setObjectName("Bold")
        self.errorLabel.setObjectName("Monospace")
       

    def setErrorMessage(self, error: str) -> None:
        self.errorLabel.setText(error)