from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont

class ConnectPage(QWidget):

    connectionRequested = Signal()
    
    def __init__(self):
        super().__init__()

        self._createWidgets()
        self._createLayout()
        self._applyStyles()

        self.setLayout(self.layout)
        
        self.connectButton.clicked.connect(self.connectionRequested.emit)
        
    def _createWidgets(self):
        self.title = QLabel("PyChat")
        self.subtitle = QLabel("idk what to write as the subtitle")
        self.connectButton = QPushButton("Connect To Server")

    def _createLayout(self):
        self.layout = QVBoxLayout()

        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)

        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.connectButton)
        self.layout.addStretch()

    def _applyStyles(self):
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title.setFont(QFont("Arial", 26))
        self.subtitle.setFont(QFont("Arial", 12))

        