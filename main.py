import sys
from PyQt6.QtWidgets import QApplication
from AuthWindow import AuthWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())