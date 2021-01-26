import cv2
import os
from PIL import Image


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile


def grayscale(image, c=3):
    """将输入图像转化为灰度图像

    :param image: numpy.array 输入图像
    :param c: int 输入图像通道数
    :return: grayscale_image
    """
    if c == 1:
        return image
    elif c == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif c == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        return None


im = cv2.imread("/home/kilox/LingXi/perception/modules/meter_recognition_v1/templates/1.jpg")
im2 = "/home/kilox/LingXi/perception/modules/meter_recognition_v1/templates/1.jpg"

im_gray = grayscale(im)
cv2.imwrite("/home/kilox/1.jpg", im_gray)
tmp_gray = cv_resize_img(im_gray, max_width=640)
cv2.imwrite("/home/kilox/2.jpg", tmp_gray)

#
# print(im.size / 1024)
#
# compress_image(im2)
# print("g")
# print(get_size(im2))
