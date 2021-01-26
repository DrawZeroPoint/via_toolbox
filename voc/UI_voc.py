import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication


class Voc(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 500)
        self.setWindowTitle('VOC scripts')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    b = Voc()
    b.show()
    sys.exit(app.exec_())
