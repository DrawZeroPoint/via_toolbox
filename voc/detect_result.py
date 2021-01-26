#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
from __future__ import division

import os
import sys
import numpy as np
import argparse
import random
import cv2
from modules import kx_detect

if "KILOX" not in os.environ:
    dir_prefix = os.path.join('/home/', 'kilox', 'KiloX', 'kiloxp')
else:
    dir_prefix = os.path.join(os.environ['KILOX'] + '/kiloxp')

if not os.path.exists(dir_prefix):
    print ("No KiloX folder under /home/$USER")
    sys.exit(1)

# Path for loading and saving images
image_dir = os.path.join(dir_prefix, 'data', 'test_data/detect_test')
roi_dir = os.path.join(dir_prefix, 'data/results/roi')
if not os.path.exists(roi_dir):
    os.makedirs(roi_dir)


def parse_args():
    """Parse input arguments

    """
    parser = argparse.ArgumentParser(description='Test detection using Faster-RCNN')

    parser.add_argument('--cuda', dest='cuda', help='whether using CUDA',
                        default=True, type=bool)

    input_args = parser.parse_args()
    return input_args


if __name__ == '__main__':
    args = parse_args()

    detect_net = kx_detect.DetectNet(args.cuda, train=False)
    img_list = os.listdir(image_dir)
    num_images = len(img_list)

    print('Loaded {} images.'.format(num_images))

    count = 0
    print(image_dir)
    for c in range(0, num_images):
        im_file = os.path.join(image_dir, img_list[c])
        im_in = np.array(cv2.imread(im_file))

        """
        仪表：'10002', 可见光异物: 70002, 刀闸：'80002', 指示器：'81002', 液位计: 82002, 湿度传感器: 83002
        """
        # Perform the detection here
        types_to_detect = [10002]
        got, bbox, rois, how_good, types_out = detect_net.detect(im_in, types_to_detect, 0.5, img_list[c])

        name = img_list[c]

        if not got:
            print ("Found nothing on %s with type: %s" % (img_list[c], types_to_detect))
            continue

        # ID, PAＴＨ, TYPE, SCORE, XMIN, YMIN, XMAX,YMAX
        for i in range(0, got):
            count = count + 1
            score = how_good[i]
            a = bbox[i][0]
            b = bbox[i][1]
            c = bbox[i][2]
            d = bbox[i][3]
            with open("/home/kilox/save.txt", "a") as f:
                f.write(str(count) + ',' + name + ',' + str(10002) + ',' + str(score) + ',' + str(a) + ',' + str(b) + ',' + str(c) + ',' + str(d) + "\n")
            f.close()
