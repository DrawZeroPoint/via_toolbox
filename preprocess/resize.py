import cv2
import os
from PIL import Image


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile


def compress_image(infile, outfile='', mb=350, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = "/home/kilox/1.jpg"
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)


def cv_resize_img(cv_image, max_width=720):
    width = cv_image.shape[1]
    if width > max_width:
        width_resized = max_width
    else:
        width_resized = width
    height_resized = int(cv_image.shape[0] * width_resized / width)
    dim = (width_resized, height_resized)
    return cv2.resize(cv_image, dim, interpolation=cv2.INTER_AREA)


img_dir = "/home/kilox/Database/Done/0_meter_recognition/pointer_dataset/images/val_pointer"
save_dir = "/home/kilox/Database/Done/0_meter_recognition/pointer_dataset/images/val_pointer_new"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
img_list = os.listdir(img_dir)

for img_item in img_list:
    file_name = os.path.join(img_dir, img_item)
    new_img = cv2.imread(file_name)
    print(file_name)
    save_name = os.path.join(save_dir, img_item)
    # if new_img.shape[1] >= 1208:
    #     new_img = cv_resize_img(new_img, max_width=1280)
    cv2.imwrite(save_name, new_img)

