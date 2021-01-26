#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------------------------
# Written by Gao Yi (yigaofire@gmail.com) and Dong Zhipeng (zhipengdongneu@gmail.com)
# This script aims to change annotation files from via forms to coco forms for digital recognition
# -------------------------------------------------------------------------------------------------

import shutil
import json
from collections import OrderedDict
import os
import logging
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import glob
import warnings
from datetime import datetime
from PIL import Image
from data import data_add_raw
import re
from coco import UI_coco
from voc import UI_voc

from os.path import expanduser

home = expanduser("~")
root_dir = os.path.join(home, "Database")
cache_dir_data = os.path.join(home, "Database/Raw/Other/data")
cache_dir_info = os.path.join(home, "Database/Raw/Other/info")

if not os.path.exists(cache_dir_data):
    os.makedirs(cache_dir_data)
if not os.path.exists(cache_dir_info):
    os.makedirs(cache_dir_info)

if not os.path.exists(root_dir):
    print("No /Database folder under /home/<user> !")
    sys.exit(1)

warnings.filterwarnings("ignore")

# log 配置 >=Debug的信息输出到stdout >=info的信息输出到log文件
logger = logging.getLogger('add_attributes')
logger.setLevel(level=logging.DEBUG)

# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# FileHandler
file_handler = logging.FileHandler('CHANGELOG.log')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def _create_image_info(image_id, file_dir, image_size, attrs_meter, attrs_flaw, attrs_security,
                       date_created=datetime.utcnow().isoformat(' ')):
    """

    :type image_id: object
    """
    image_info = OrderedDict({
        "id": image_id,
        "file_dir": file_dir,
        "width": image_size[0],
        "height": image_size[1],
        "date_created": date_created,
        "attrs_meter": attrs_meter,
        "attrs_flaw": attrs_flaw,
        "attrs_security": attrs_security,
    })

    return image_info


def is_image(name):
    if os.path.splitext(name)[1] == '.png' or os.path.splitext(name)[1] == '.jpg':
        return True
    else:
        return False


def is_info(name):
    return os.path.splitext(name)[1] == '.json'


class YaoChi(QWidget):
    """针对单张图片或文件夹中所有图片为其添加属性
    """

    def __init__(self):
        super().__init__()
        self.init_ui()
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 被选文件夹绝对路径
        self.source_dir = None
        self.img_name = None
        self.text = None
        self.search_keywords = None

    def init_ui(self):

        self.setGeometry(0, 0, 1000, 500)
        self.setWindowTitle('VIA Toolbox')
        self.setWindowIcon(QIcon('source/perxeption.png'))

        # 设置当前页
        self.currentPage = 1
        # 得到总页数
        self.totalPage = 1

        # 文件加载
        self.open_img_bt = QPushButton('Open Img', self)
        self.folder_bt = QPushButton('Open Dir', self)

        self.img_bg_lb = QLabel(self)

        # 图片切换
        self.pre_img_bt = QPushButton('Prev Img', self)
        self.next_img_bt = QPushButton('Next Img', self)
        self.select_bt = QPushButton('Normal Attrs', self)
        self.add_attr_bt = QPushButton('Add Attrs', self)

        self.quit_bt = QPushButton('Quit', self)

        self.select_bg_lb = QLabel(self)

        # layout config
        self.open_img_bt.move(20, 10)
        self.folder_bt.move(20, 50)

        self.img_bg_lb.setFixedSize(340, 380)
        self.img_bg_lb.move(330, 25)
        self.img_bg_lb.setStyleSheet("QLabel{background:white;}")
        k = QtGui.QPixmap('source/python.png').width() / self.img_bg_lb.width()
        pixmap = QPixmap('source/python.png').scaled(self.img_bg_lb.width(), QtGui.QPixmap('source/python.png').width() / k)
        self.img_bg_lb.setPixmap(pixmap)

        self.pre_img_bt.move(390, 430)
        self.next_img_bt.move(530, 430)
        self.select_bt.move(20, 85)
        self.add_attr_bt.move(20, 273)

        self.quit_bt.move(920, 0)

        # 复选框背景
        self.select_bg_lb.setFixedSize(300, 150)
        self.select_bg_lb.move(20, 120)
        self.select_bg_lb.setStyleSheet("QLabel{background:white;}")

        # 属性复选框
        # 表计类
        self.meter_0_cb = QCheckBox('meter detection', self)
        self.meter_0_cb.move(20, 120)

        self.meter_pointer_cb = QCheckBox('pointer meter', self)
        self.meter_pointer_cb.move(40, 140)

        self.meter_digital_cb = QCheckBox('digital meter', self)
        self.meter_digital_cb.move(160, 140)

        self.meter_breaker_cb = QCheckBox('breaker', self)
        self.meter_breaker_cb.move(40, 160)

        self.meter_liquidometer_cb = QCheckBox('liquidometer', self)
        self.meter_liquidometer_cb.move(160, 160)

        # 缺陷检测类
        self.flaw_0_cb = QCheckBox('defect detection', self)
        self.flaw_0_cb.move(20, 190)

        # 安全生产类
        self.security_0_cb = QCheckBox('security detection', self)
        self.security_0_cb.move(20, 220)

        # self.security_1_cb = QCheckBox('服装', self)
        # self.security_1_cb.move(40, 245)

        # self.security_2_cb = QCheckBox('安全帽', self)
        # self.security_2_cb.move(160, 245)

        self.create_info_bt = QPushButton('Create Info', self)
        self.create_info_bt.move(20, 460)

        # 添加新的属性
        self.add_attrs_tb = QTextBrowser(self)
        self.add_attrs_tb.move(20, 300)
        self.add_attrs_tb.resize(300, 150)

        self.input_keywords_bt = QPushButton('Input keywords', self)
        self.input_keywords_bt.move(700, 43)

        self.search_bt = QPushButton('Search', self)
        self.search_bt.move(885, 120)

        # 查询下载数据集到本地硬盘
        self.search_tb = QTextBrowser(self)
        self.search_tb.move(700, 70)
        self.search_tb.resize(270, 50)

        # 添加数据库
        self.add_raw_bt = QPushButton('Add_raw_data', self)
        self.add_raw_bt.move(190, 460)

        # 数据集操作脚本界面链接
        self.coco_bt = QPushButton('coco', self)
        self.coco_bt.move(700, 200)

        self.voc_bt = QPushButton('voc', self)
        self.voc_bt.move(850, 200)

        self.show()

        self.open_img_bt.clicked.connect(self._open_image)
        self.folder_bt.clicked.connect(self._folder)
        self.pre_img_bt.clicked.connect(self.pre_img)
        self.next_img_bt.clicked.connect(self.next_img)
        self.add_attr_bt.clicked.connect(self._add_attr)
        self.input_keywords_bt.clicked.connect(self._search)

        self.quit_bt.clicked.connect(QCoreApplication.instance().quit)
        self.quit_bt.resize(self.quit_bt.sizeHint())
        self.create_info_bt.clicked.connect(self.go)
        self.search_bt.clicked.connect(self.search)
        self.add_raw_bt.clicked.connect(self._add_raw_data)

        self.meter_0_cb.stateChanged.connect(self._change_meter1)
        self.meter_pointer_cb.stateChanged.connect(self._change_meter2)
        self.meter_digital_cb.stateChanged.connect(self._change_meter2)
        self.meter_breaker_cb.stateChanged.connect(self._change_meter2)
        self.meter_liquidometer_cb.stateChanged.connect(self._change_meter2)

        # self.security_0_cb.stateChanged.connect(self._change_security1)
        # self.security_1_cb.stateChanged.connect(self._change_security2)
        # self.security_2_cb.stateChanged.connect(self._change_security2)

    # 刷新状态
    def _update_status(self):
        if self.source_dir:
            print("Img number :%d" % (self.currentPage + 1))

            # 设置按钮是否可用
            if self.currentPage == 0:
                self.pre_img_bt.setEnabled(False)
                self.next_img_bt.setEnabled(True)
            elif self.currentPage == self.totalPage - 1:
                self.pre_img_bt.setEnabled(True)
                self.next_img_bt.setEnabled(False)
            else:
                self.pre_img_bt.setEnabled(True)
                self.next_img_bt.setEnabled(True)
        else:
            self.pre_img_bt.setEnabled(False)
            self.next_img_bt.setEnabled(False)
        self.meter_0_cb.setTristate(False)
        self.meter_0_cb.setCheckState(Qt.Unchecked)
        self.flaw_0_cb.setTristate(False)
        self.flaw_0_cb.setCheckState(Qt.Unchecked)
        self.security_0_cb.setTristate(False)
        self.security_0_cb.setCheckState(Qt.Unchecked)

    def show_image(self, c):
        if self.source_dir is None:
            pass
        else:
            img_list = sorted(glob.glob(self.source_dir + "/*jpg") + glob.glob(self.source_dir + "/*png"))
            self.img_name = os.path.join(self.source_dir, img_list[c])
            k = QtGui.QPixmap(self.img_name).width() / self.img_bg_lb.width()
            jpg = QtGui.QPixmap(self.img_name).scaled(self.img_bg_lb.width(), QtGui.QPixmap(self.img_name).width() / k)
            self.img_bg_lb.setPixmap(jpg)

    # 前一页按钮按下
    def pre_img(self):
        if self.img_name is not None:
            self._info_creator(self.img_name)
        self.currentPage -= 1
        self._update_status()
        self.show_image(self.currentPage)

    # 后一页按钮按下
    def next_img(self):
        if self.img_name is not None:
            self._info_creator(self.img_name)
        self.currentPage += 1
        self._update_status()
        self.show_image(self.currentPage)

    def _open_image(self):
        self.img_name, img_type = QFileDialog.getOpenFileName(self, "Open source", "", "*.jpg;;*.png;;All Files(*)")
        if not self.img_name:
            pass
        else:
            k = QtGui.QPixmap(self.img_name).width() / self.img_bg_lb.width()
            jpg = QtGui.QPixmap(self.img_name).scaled(self.img_bg_lb.width(), QtGui.QPixmap(self.img_name).width() / k)
            self.img_bg_lb.setPixmap(jpg)

    def _folder(self):

        self.source_dir = QFileDialog.getExistingDirectory(self, "Open dir", "./")  # 起始路径

        if self.source_dir is None:
            QMessageBox.information(self, 'YaoChi:', 'No images')
        else:
            img_list = sorted(glob.glob(self.source_dir + "/*jpg") + glob.glob(self.source_dir + "/*png"))
            self.totalPage = len(img_list)
            print('Loaded {} images.'.format(self.totalPage))
            if len(img_list) == 0:
                QMessageBox.information(self, 'YaoChi:', 'No images')
            else:
                c = 0
                self.show_image(c)
                self._update_status()

    def retrieve_page(self, page):
        if page == -1:
            if self.cur_page == 1: return
            self.cur_page -= 1
        elif page == -2:
            if self.cur_page == self.total_pages: return
            self.cur_page += 1

    def _change_meter1(self):
        if self.meter_0_cb.checkState() == Qt.Checked:
            self.meter_pointer_cb.setChecked(True)
            self.meter_digital_cb.setChecked(True)
            self.meter_breaker_cb.setChecked(True)
            self.meter_liquidometer_cb.setChecked(True)
        elif self.meter_0_cb.checkState() == Qt.Unchecked:
            self.meter_pointer_cb.setChecked(False)
            self.meter_digital_cb.setChecked(False)
            self.meter_breaker_cb.setChecked(False)
            self.meter_liquidometer_cb.setChecked(False)

    def _change_meter2(self):
        if self.meter_pointer_cb.isChecked() and self.meter_digital_cb.isChecked() \
                and self.meter_breaker_cb.isChecked() and self.meter_liquidometer_cb.isChecked():
            self.meter_0_cb.setCheckState(Qt.Checked)
        elif self.meter_pointer_cb.isChecked() or self.meter_digital_cb.isChecked() \
                or self.meter_breaker_cb.isChecked() or self.meter_liquidometer_cb.isChecked():
            self.meter_0_cb.setTristate()
            self.meter_0_cb.setCheckState(Qt.PartiallyChecked)
        else:
            self.meter_0_cb.setTristate(False)
            self.meter_0_cb.setCheckState(Qt.Unchecked)

    def _change_security1(self):
        if self.security_0_cb.checkState() == Qt.Checked:
            self.security_1_cb.setChecked(True)
            self.security_2_cb.setChecked(True)
        elif self.security_0_cb.checkState() == Qt.Unchecked:
            self.security_1_cb.setCheckable(False)
            self.security_2_cb.setCheckable(False)

    def _change_security2(self):
        if self.security_1_cb.isChecked() and self.security_2_cb.isChecked():
            self.security_0_cb.setCheckState(Qt.Checked)
        elif self.security_1_cb.isChecked() or self.security_2_cb.isChecked():
            self.security_0_cb.setTristate()
            self.security_0_cb.setCheckState(Qt.PartiallyChecked)
        else:
            self.security_0_cb.setTristate(False)
            self.security_0_cb.setCheckState(Qt.Unchecked)

    def go(self):
        if self.img_name is not None:
            self._info_creator(self.img_name)
        QMessageBox.information(self, 'YaoChi:', 'Info Created ')

    def _add_attr(self):
        self.attrs_text, ok = QInputDialog.getMultiLineText(self, 'Others', ' Aim:Content')
        if ok:
            self.add_attrs_tb.setText(self.attrs_text)

    def _search(self):
        self.search_text, ok = QInputDialog.getMultiLineText(self, 'Search', ' Input keywords')
        if ok:
            self.search_tb.setText(self.search_text)
            self.search_keywords = self.search_text

    def _info_creator(self, img_name):
        INFO = OrderedDict({
            "description": "Information  of YaoChi Dataset",
            "version": "0.1.0",
            "Toolbox url": "ssh://git@172.16.2.5:30001/PerXeption/Toolbox.git",
            "year": 2019, "contributor": "Kilox PreXeption Group",
            "date_created": datetime.utcnow().isoformat(' ')
        })
        info_output = OrderedDict({
            "info": INFO,
            "images": [],
            "attrs": []
        })
        info_name = os.path.splitext(img_name)[0] + '.json'
        image = Image.open(img_name)
        # if self.source_dir :
        #     pass
        # else:
        image_id = self.currentPage

        attrs_meter = []
        if self.meter_pointer_cb.isChecked():
            attrs_meter.append("pointer meter")
        if self.meter_digital_cb.isChecked():
            attrs_meter.append("digital meter")
        if self.meter_breaker_cb.isChecked():
            attrs_meter.append("breaker")
        if self.meter_liquidometer_cb.isChecked():
            attrs_meter.append("liquidometer")
        attrs_flaw = []
        if self.flaw_0_cb.isChecked():
            attrs_flaw.append("defect detection")
        attrs_security = []
        if self.security_0_cb.isChecked():
            attrs_security.append("security detection")

        image_info = _create_image_info(
            image_id, img_name, image.size, attrs_meter, attrs_flaw, attrs_security)
        info_output["images"].append(image_info)

        attrs = {}
        if self.text is not None:
            for s in self.text.split():
                pos = s.find(':')
                key = s[:pos]
                value = s[pos + 1:]
                attrs[key] = value

        info_output["attrs"].append(attrs)
        with open('{}'.format(info_name), 'w') as output_json_file:
            json.dump(info_output, output_json_file)

    def _add_raw_data(self):
        images = []
        infos = []
        if self.source_dir:
            for image in os.listdir(self.source_dir):
                if is_image(image):
                    image = os.path.join(self.source_dir, image)
                    images.append(image)
            infos = [os.path.join(self.source_dir, info) for info in os.listdir(self.source_dir) if is_info(info)]
        else:
            images.append(self.img_name)
            info_name = os.path.splitext(self.img_name)[0] + '.json'
            infos.append(info_name)

        logger.info('read image({}){}... info({}){}... '.format(len(images), images[0:5], len(infos), infos[0:5]))
        # 插入的info列表应该是所有images的所有元素修改后缀名得到
        infos = [os.path.splitext(image)[0] + '.json' for image in images]

        image_dir = os.path.join(home, 'Database/Raw/Visual/Image')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        target_dir = data_add_raw.TargetDir(image_dir)
        target_dir.insert_data(source_data=images, source_info=infos)

        QMessageBox.information(self, 'YaoChi:', 'Done')

    def search(self):
        if self.search_keywords:
            if self.source_dir:
                for image in os.listdir(self.source_dir):
                    if is_image(image):
                        img_target = os.path.join(cache_dir_data, image)
                        info_target = os.path.join(cache_dir_info, os.path.splitext(image)[0] + '.json')
                        image_dir = os.path.join(self.source_dir, image)
                        info_dir = self.source_dir.replace('/data', '/info')
                        info_dir = os.path.join(info_dir, os.path.splitext(image)[0] + '.json')
                        file_str = open(info_dir)
                        setting = json.load(file_str, object_pairs_hook=OrderedDict)
                        get_obj = json.dumps(setting)
                        info = re.findall(self.search_keywords, get_obj)
                        if info:
                            shutil.copyfile(image_dir, img_target)
                            shutil.copyfile(info_dir, info_target)
                            QMessageBox.information(self, 'YaoChi:', 'Search Done')
                        else:
                            QMessageBox.information(self, 'YaoChi:', 'Mismatch')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = YaoChi()
    b = UI_coco.Coco()
    c = UI_voc.Voc()
    a.show()
    a.coco_bt.clicked.connect(b.show)
    a.voc_bt.clicked.connect(c.show)
    sys.exit(app.exec_())
