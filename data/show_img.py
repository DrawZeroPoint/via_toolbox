#!/usr/bin/env python
# -*-encoding:utf-8 -*-

import cv2
import argparse


def parse_args():
    """Parse input arguments

    """
    parser = argparse.ArgumentParser(prog='show_img', description='', epilog='')
    parser.add_argument('id', help='')
    input_args = parser.parse_args()
    return input_args


def print_loc(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print('x, y: ', x, y)


if __name__ == '__main__':
    args = parse_args()
    img = cv2.imread('./{}.jpg'.format(args.id))

    win_name = 'source-{}'.format(args.id)
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, print_loc)

    while (1):
        cv2.imshow(win_name, img)
        k = cv2.waitKey(20)
        if k == 27:
            break

    cv2.destroyAllWindows()
