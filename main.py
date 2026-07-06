import sys
from PySide6.QtWidgets import QApplication
from application import Application


def main():
    qtApp = QApplication(sys.argv)
    app = Application(qtApp)
    app.run()
    
    
if __name__ == "__main__":
    main()   


