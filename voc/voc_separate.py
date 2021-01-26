import numpy as np
import os


def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path)]


def seperate(path):
    """读取图片名字,按比例写入文件xml_list.txt 与　test.txt

    :param path:
    :return:
    """
    directorys = get_imlist(path)
    train = open('./cache/xml_list.txt', 'w')
    test = open('./cache/test.txt', 'w')
    scale = 0.001
    lens = len(directorys) * scale
    count = 0 - lens
    for directory in directorys:
        if not (directory.endswith('.jpg') or directory.endswith('.png') or directory.endswith('.JPG')):
            pass
        else:
            filename = directory[directory.rfind("/") + 1:]
            img_name = os.path.splitext(filename)[0]
            if count <= 0:
                test.write(img_name + ".xml" + "\n")
            else:
                train.write(img_name + ".xml" + "\n")
            count = count + 1
    train.close
    test.close


if __name__ == '__main__':
    seperate("/media/kilox/dfbf936d-378b-41a1-a558-cc1f504bbfd0/datasets/kilox_meter_dataset/meter/JPEGImages")
