from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtWidgets import QWidget, QLabel, QProgressBar, QVBoxLayout


class LoadingPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self._createWidgets()
        self._createLayout()
        self._applyStyles()
        
        self.setLayout(self.layout)
        
    def _createWidgets(self):
        self.title = QLabel("Loading...")
        self.loadingBar = QProgressBar()
        
        self.loadingBar.setRange(0, 0)
        
    def _createLayout(self):
        self.layout = QVBoxLayout()

        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.loadingBar)
        self.layout.addStretch()
        
    def _applyStyles(self):
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loadingBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 26))