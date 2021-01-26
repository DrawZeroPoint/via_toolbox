import sys
from PyQt5.QtWidgets import *
import coco.coco_digit_25 as coco_digit_25
import coco.coco_multi_obj as coco_multi_obj
from PyQt5.QtCore import Qt


class Coco(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.image_dir = None
        self.annotation_dir = None

    def initUI(self):
        self.setGeometry(0, 0, 1000, 500)
        self.setWindowTitle('coco scripts')

        self.img_bg_lb = QLabel(self)
        self.img_bg_lb.setFixedSize(230, 120)
        self.img_bg_lb.move(20, 10)
        self.img_bg_lb.setStyleSheet("QLabel{background:white;}")

        self.img_bg_lb = QLabel(self)
        self.img_bg_lb.setFixedSize(230, 30)
        self.img_bg_lb.move(20, 10)
        self.img_bg_lb.setStyleSheet("QLabel{background:gray;}")
        self.img_bg_lb.setText("covert to coco format")
        self.img_bg_lb.setAlignment(Qt.AlignCenter)
        self.img_bg_lb.adjustSize()

        # 文件加载
        self.image_dir_bt = QPushButton('imgs_dir', self)
        self.image_dir_bt.move(150, 50)

        self.annotation_dir_bt = QPushButton('ann_dir', self)
        self.annotation_dir_bt.move(20, 50)

        self.convert_bt = QPushButton('convert', self)
        self.convert_bt.move(85, 100)

        self.image_dir_bt.clicked.connect(self._image)
        self.annotation_dir_bt.clicked.connect(self._annotation)
        self.convert_bt.clicked.connect(self._to_coco)

    def _image(self):
        self.image_dir = QFileDialog.getExistingDirectory(self, "Open dir", "./")  # 原图像路径
        QMessageBox.information(self, 'YaoChi:', self.image_dir)

    def _annotation(self):
        self.annotation_dir, img_type = QFileDialog.getOpenFileName(self, "Open source", "", "*.json;;All Files(*)")
        QMessageBox.information(self, 'YaoChi:', self.annotation_dir)

    def _to_coco(self):

        if self.image_dir and self.annotation_dir:
            # coco_digit_25.run(self.image_dir, self.annotation_dir)
            coco_multi_obj.run(self.image_dir, self.annotation_dir)
            QMessageBox.information(self, 'YaoChi:', 'Converted, new file is in annotation_dir')
        else:
            QMessageBox.information(self, 'YaoChi:', 'Select Dirs')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    b = Coco()
    b.show()
    sys.exit(app.exec_())
