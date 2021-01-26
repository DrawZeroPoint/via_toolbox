import json
import re
import fnmatch
from PIL import Image
from pylab import *
import os
import warnings

warnings.filterwarnings("ignore")
num_keypoints = 5

"""
由via标注的５个关键点转成coco格式５个关键点，visible默认为２，
"""

IMAGE_DIR = "/home/gy/Database/Done/grape/coco/train2017"
ANNOTATION_DIR = "/home/gy/Database/Done/grape/coco/annotations/via_export_json.json"
save_dir = "/home/gy/Database/Done/grape/coco/annotations/ann_train_pointer.json"
INFO = {
    "description": "Keypoints Location of Pointer Dataset",
    "url": "https://yigaoyi.github.io/",
    "version": "1.0",
    "year": 2020,
    "contributor": "Kilox PerXeption Group",
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
        'keypoints': ["p_one", "p_two", "p_three", "p_four", "p_five"],
        'skeleton': [[1, 2], [2, 3], [3, 4], [4, 5]]
    }
]


class FC:
    """For a colorful print
    DO NOT CHANGE 'ROS', we need a uniform style in ROS
    """
    HEADER = '\033[1m\033[95m[KiloX Pointer]: '
    OKBLUE = '\033[1m\033[94m[KiloX Pointer]: '
    OKGREEN = '\033[1m\033[92m[KiloX Pointer]: '
    WARN = '\033[1m\033[93m[KiloX Pointer]: '
    FAIL = '\033[1m\033[91m[KiloX Pointer]: '
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        pass


def filter_for_jpeg(root, files):
    """filter jpg files in dictionary

    :param root:
    :param files:
    :return:
    """
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    return files


def create_image_info(image_id, file_name, image_size,
                      date_captured=datetime.datetime.utcnow().isoformat(' '),
                      license_id=1, coco_url="", flickr_url=""):
    image_info = {
        "id": image_id,
        "file_name": file_name,
        "width": image_size[0],
        "height": image_size[1],
        "date_captured": date_captured,
        "license": license_id,
        "coco_url": coco_url,
        "flickr_url": flickr_url
    }

    return image_info


def create_annotation_info(annotation_id, image_id, category_info, binary_mask, keypoints, num_keypoints,
                           image_size=None, tolerance=2, bounding_box=None, ):
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_info["id"],
        "iscrowd": 0,
        "area": 0,
        "bbox": bounding_box.tolist(),
        "segmentation": [],
        "num_keypoints": num_keypoints,
        "keypoints": keypoints
    }

    return annotation_info


def main():
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    count = 0
    for root, _, files in os.walk(IMAGE_DIR):
        image_files = filter_for_jpeg(root, files)
        # go through each image
        for image_filename in image_files:
            print(image_filename)
            image = Image.open(image_filename)
            index = image_filename.rfind('.')
            afdex = image_filename.rfind('/')
            image_id = int(image_filename[afdex + 1:index])
            image_id = "%d" % image_id
            image_id = int(image_id)
            image_info = create_image_info(
                image_id, os.path.basename(image_filename), image.size)
            coco_output["images"].append(image_info)

            file_str = open(ANNOTATION_DIR)
            setting = json.load(file_str)
            get_obj = json.dumps(setting)
            info = re.findall(image_filename[afdex + 1:index] + r'.jpg+\d+', get_obj)
            if not info:
                print("{} is not exit in annotations!".format(image_filename))
            else:
                count = count + 1

                obj_str = json.dumps(setting["".join(info)])

                a = int("".join(re.findall(r"\"x\"\: (.+?)\,", obj_str)))
                b = int("".join(re.findall(r"\"y\"\: (.+?)\,", obj_str)))
                try:
                    c = int("".join(re.findall(r"\"width\"\: (.+?)\,", obj_str)))
                    d = int("".join(re.findall(r"\"height\"\: (.+?)\}", obj_str)))
                except ValueError:
                    c = int("".join(re.findall(r"\"width\"\: (.+?)\}", obj_str)))
                    d = int("".join(re.findall(r"\"height\"\: (.+?)\,", obj_str)))
                bbox = [a, b, c, d]
                x = a + c
                y = c + d
                segmentation = [x, y, a, y, a, b, x, b, x, y]
                try:
                    px_1 = int(re.findall(r"\"cx\"\: (.+?)\,", obj_str)[0])
                    py_1 = int(re.findall(r"\"cy\"\: (.+?)\,", obj_str)[0])
                    px = re.findall(r"\"cx\"\: (.+?)\,", obj_str)
                    py = re.findall(r"\"cy\"\: (.+?)\}", obj_str)
                except ValueError:
                    # print("g")
                    try:
                        px_1 = int(re.findall(r"\"cx\"\: (.+?)\}", obj_str)[0])
                        py_1 = int(re.findall(r"\"cy\"\: (.+?)\,", obj_str)[0])
                        px = re.findall(r"\"cx\"\: (.+?)\}", obj_str)
                        py = re.findall(r"\"cy\"\: (.+?)\,", obj_str)
                    except ValueError:
                        # print("y")
                        px_1 = int(re.findall(r"\"cx\"\: (.+?)\,", obj_str)[0])
                        py_1 = int(re.findall(r"\"cy\"\: (.+?)\}", obj_str)[0])
                        px = re.findall(r"\"cx\"\: (.+?)\,", obj_str)
                        py = re.findall(r"\"cy\"\: (.+?)\}", obj_str)

                # visible = re.findall(r"\"visible\"\: \"(.+?)\"", obj_str)
                # if not len(visible) - len(px) == 1:
                #     print(FC.WARN + "Label info is wrong!" + FC.END)
                points = []
                for i in arange(5):
                    # if visible[i] == '0':
                    #     points.append(0)
                    #     points.append(0)
                    #     points.append(0)
                    # else:
                    #     print(px[i])
                    points.append(int(px[i]))
                    points.append(int(py[i]))
                    points.append(2)
                    # points.append(int(visible[i]))

                annotation_info = {
                    "id": count,
                    "image_id": image_id,
                    "category_id": 1,
                    "iscrowd": 0,
                    "area": c * d,
                    "bbox": bbox,
                    "segmentation": segmentation,
                    "num_keypoints": num_keypoints,
                    "keypoints": points
                }
                coco_output["annotations"].append(annotation_info)

    with open('{}'.format(save_dir), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
