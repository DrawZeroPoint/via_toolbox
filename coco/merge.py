#!/usr/bin/env python
# encoding: utf-8

import os  
import datetime
from os.path import join as pjoin
import json

output_dir = '/home/kilox/labeldata'     
listdir = os.listdir(output_dir)
INFO = {
    "description": "Meter Dataset",
    "url": "https://yigaoyi.github.io/",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "Kilo Arithmetic",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'pointer',
        'supercategory': 'pointer',
        'keypoints': ["begin","one","center","two","end"],
        'skeleton': [[1,2],[2,3],[3,4],[4,5]]
    }
]

fr = open("/home/kilox/labeldata/test.json") 
model=json.load(fr)
fr.close()
f = open("/home/kilox/labeldata/meter_.json")  
setting = json.load(f)
f.close()

img1 = setting['images']  
img2 = model['images']
img = img1 + img2
  
ann1 = setting['annotations']  
ann2 = model['annotations']
ann = ann1 + ann2

coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": img,
        "annotations": ann
    }


jsObj = json.dumps(model)    

with open(pjoin(output_dir, '{}/test.json'.format("/home/kilox/labeldata")), "w") as fw:  
    # fw.write(jsObj)  
    # fw.close()
    json.dump(coco_output, fw)

