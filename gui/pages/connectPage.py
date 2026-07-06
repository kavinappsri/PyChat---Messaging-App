from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PySide6.QtGui import QFont, QIntValidator

class ConnectPage(QWidget):

    connectionRequested = Signal(str, int)
    
    def __init__(self):
        super().__init__()

        self._createWidgets()
        self._createLayout()
        self._applyStyles()

        self.setLayout(self.layout)
        
        self.connectButton.clicked.connect(lambda: self.connectionRequested.emit(
            self.ipEdit.text(), 
            int(self.portEdit.text())
        ))
        
    def _createWidgets(self):
        self.title = QLabel("PyChat")
        self.subtitle = QLabel("idk what to write as the subtitle")
        self.connectButton = QPushButton("Connect To Server")
        self.ipEdit = QLineEdit()
        self.portEdit = QLineEdit()
        
        self.ipEdit.setPlaceholderText("Server IP")
        self.portEdit.setPlaceholderText("Server Port")
        
        self.portEdit.setValidator(QIntValidator(1, 65535))

    def _createLayout(self):
        self.layout = QVBoxLayout()

        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)

        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.ipEdit)
        self.layout.addWidget(self.portEdit)
        self.layout.addWidget(self.connectButton)
        self.layout.addStretch()

    def _applyStyles(self):
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title.setFont(QFont("Arial", 26))
        self.subtitle.setFont(QFont("Arial", 12))

        