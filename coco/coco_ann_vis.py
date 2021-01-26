# -*- coding:utf-8 -*-
from __future__ import print_function

from pycocotools.coco import COCO
import json
import os
import skimage.io as io
import matplotlib.pyplot as plt
import pylab

pylab.rcParams['figure.figsize'] = (8.0, 10.0)
cache_dir = "./cache"
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)


def get_one_ann(ann_file, n):
    """获取第n张图像的注释文档，并保存在./cache文件夹下
    :param n: 图像在注释文档中的序号数
    :param ann_file: coco注释文档
    :return:
    """

    data = json.load(open(ann_file, 'r'))

    # 只提取第一张图片
    data_2 = {'info': data['info'], 'licenses': data['licenses'], 'images': [data['images'][n]],
              'categories': data['categories']}
    annotation = []

    # 通过img_i_d 找到其所有对象
    img_i_d = data_2['images'][0]['id']
    for ann in data['annotations']:
        if ann['image_id'] == img_i_d:
            annotation.append(ann)

    data_2['annotations'] = annotation

    # 保存到新的JSON文件，便于查看数据特点
    # indent=4 更加美观显示
    json.dump(data_2, open('/home/kilox/Database/Done/1_general_det/meter_coo/example_instances_val2017.json', 'w'), indent=4)


def show_ann(img_dir):
    """显示./cache文件夹中提取的注释文档
    :param img_dir: 原图像所在地址
    :return:
    """
    ann_file = './cache/example_instances_val2017.json'
    coco = COCO(ann_file)

    # display COCO categories and supercategories
    cats = coco.loadCats(coco.getCatIds())
    nms = [cat['name'] for cat in cats]
    print('COCO categories: \n{}\n'.format(' '.join(nms)))

    nms = set([cat['supercategory'] for cat in cats])
    print('COCO supercategories: \n{}'.format(' '.join(nms)))

    img_ids = coco.getImgIds()
    img = coco.loadImgs(img_ids[0])[0]
    I = io.imread('%s/%s' % (img_dir, img['file_name']))

    # load and display instance annotations
    # catIds = coco.getCatIds(catNms=['person','dog','skateboard']);
    # catIds=coco.getCatIds()
    cat_ids = []
    for ann in coco.dataset['annotations']:
        if ann['image_id'] == img_ids[0]:
            cat_ids.append(ann['category_id'])

    plt.imshow(I)
    plt.axis('off')

    ann_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
    anns = coco.loadAnns(ann_ids)
    coco.showAnns(anns)

    # initialize COCO api for person keypoints annotations
    # ann_file = '{}/annotations/person_keypoints_{}.json'.format(img_dir, data_type)
    # coco_kps = COCO(ann_file)

    # # 加载肢体关键点
    # plt.imshow(I)
    # plt.axis('off')
    # ax = plt.gca()
    # ann_ids = coco_kps.getAnnIds(imgIds=source['id'], catIds=cat_ids, iscrowd=None)
    # anns = coco_kps.loadAnns(ann_ids)
    # coco_kps.showAnns(anns)

    # # initialize COCO api for caption annotations
    # ann_file = '{}/annotations/captions_{}.json'.format(img_dir, data_type)
    # coco_caps = COCO(ann_file)

    # # 加载文本描述
    # ann_ids = coco_caps.getAnnIds(imgIds=source['id']);
    # anns = coco_caps.loadAnns(ann_ids)
    # coco_caps.showAnns(anns)
    #
    plt.imshow(I)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    # ann_file = '/home/kilox/Database/Toolbox/cache/train.json'
    # img_dir = '/home/kilox/Downloads/表計類型'

    ann_file = '/home/kilox/Database/Done/1_general_det/meter_coo/annotations/ann_train_pointer.json'
    img_dir = '/home/kilox/Database/Done/1_general_det/meter_coo/image'
    get_one_ann(ann_file, 1)
    show_ann(img_dir)
