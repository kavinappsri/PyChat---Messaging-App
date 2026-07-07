from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class ErrorPage(QWidget):
    def __init__(self):
        super().__init__()
        
    def _createWidgets(self):
        self.title = QLabel("Oops! We've hit an error!")
        self.errorLabel = QLabel()
        self.okButton = QPushButton("OK")
        
    def _createLayout(self):
        self.layout = QVBoxLayout()
        
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.errorLabel)
        self.layout.addWidget(self.okButton)
        
    def _applyStyles(self):
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title.setFont(QFont("Arial", 26))
        self.errorLabel.setFont(QFont("Arial", 12))