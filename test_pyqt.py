import sys
from PyQt6.QtWidgets import QApplication, QWidget

def main():
    app=QApplication(sys.argv)
    window=QWidget()
    window.resize(400,200)
    window.setWindowTitle("PyQt6 Test")
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()