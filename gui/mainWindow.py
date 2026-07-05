from PySide6.QtWidgets import QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyChat")
        self.resize(900, 600)