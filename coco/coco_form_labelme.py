import json
from coco_image import img_b64_to_arr
import PIL.Image
import PIL.ImageDraw
from pylab import *
import glob

INFO = {
    "description": "COCO format Dataset",
    "url": "http://172.16.2.5:30000/PerXeption/Toolbox",
    "version": "0.1.0",
    "year": 2019,
    "contributor": "PreXeption Group",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]


def mask_2_box(mask):
    '''从mask反算出其边框
    mask：[h,w]  0、1组成的图片
    1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
    '''
    index = np.argwhere(mask == 1)
    rows = index[:, 0]
    clos = index[:, 1]
    # 解析左上角行列号
    left_top_r = np.min(rows)  # y
    left_top_c = np.min(clos)  # x

    # 解析右下角行列号
    right_bottom_r = np.max(rows)
    right_bottom_c = np.max(clos)

    return [left_top_c, left_top_r, right_bottom_c - left_top_c,
            right_bottom_r - left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式


def polygons_to_mask(img_shape, polygons):
    mask = np.zeros(img_shape, dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    xy = list(map(tuple, polygons))
    PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


class Convert(object):
    """转换labelme的数据集格式为coco 数据集格式

    """

    def __init__(self, labelme_ann, save_json_path):
        """
        :param labelme_ann: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        """
        self.images = []
        self.categories = []
        self.annotations = []
        self.data_coco = self.data_2_coco()
        self.labelme_json = labelme_ann
        self.save_json_path = save_json_path
        self.label = []
        self.annID = 1
        self.height = 0
        self.width = 0

        self.save_json()

    def data_transfer(self):
        for num, json_file in enumerate(self.labelme_json):
            with open(json_file, 'r') as fp:
                data = json.load(fp)
                self.images.append(self.image(data, num))
                for shapes in data['shapes']:
                    label = shapes['label'].split(',')
                    if label[0] not in self.label:
                        self.categories.append(self.categorie(label))
                        self.label.append(label[0])
                    points = shapes['points']
                    self.annotations.append(self.annotation(points, label, num))
                    self.annID += 1

    def image(self, data, num):
        image = {}
        # 解析原图片数据
        img = img_b64_to_arr(data['imageData'])

        height, width = img.shape[:2]
        image['license'] = 1
        image['file_name'] = data['imagePath'].split('/')[-1]
        image['coco_url'] = ""
        image['height'] = height
        image['width'] = width
        image['date_captured'] = ""
        image['flickr_url'] = ""
        image['id'] = int(num + 1)

        self.height = height
        self.width = width

        return image

    def categorie(self, label):

        categorie = {'supercategory': label[0], 'id': len(self.label) + 1}

        if len(label) == 1:
            categorie['name'] = label[0]
        elif len(label) == 2:
            categorie['name'] = label[1]
        else:
            print("label is wrong", label)
        return categorie

    def annotation(self, points, label, num):
        annotation = {'iscrowd': 0, 'image_id': int(num + 1), 'bbox': list(map(float, self.get_bbox(points)))}
        # 由点形成segmentation
        # annotation['segmentation']=[list(np.asarray(points).flatten())]

        # 由bbox形成segmentation
        x = annotation['bbox'][0]
        y = annotation['bbox'][1]
        w = annotation['bbox'][2]
        h = annotation['bbox'][3]
        annotation['segmentation'] = [[x, y, x + w, y, x + w, y + h, x, y + h]]

        annotation['category_id'] = self.get_cat_id(label)
        annotation['id'] = int(self.annID)
        # add area info
        annotation['area'] = self.height * self.width  # 这里用了原图的长和宽，并不是bbox的面积；但对检测任务不影响
        return annotation

    def get_cat_id(self, label):
        for categorise in self.categories:
            if len(label) == 1 and label[0] == categorise['name']:
                return categorise['id']
            elif len(label) == 2 and label[1] == categorise['name']:
                return categorise['id']
        return -1

    def get_bbox(self, points):
        polygons = points
        mask = polygons_to_mask([self.height, self.width], polygons)
        return mask_2_box(mask)

    def data_2_coco(self):
        data_coco = {"info": INFO, "licenses": LICENSES, "images": self.images, "categories": self.categories,
                     "annotations": self.annotations}
        return data_coco

    def save_json(self):
        self.data_transfer()
        json.dump(self.data_coco, open(self.save_json_path, 'w', encoding='utf-8'), indent=4, separators=(',', ': '),
                  cls=MyEncoder)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


if __name__ == "__main__":
    labelme_json = glob.glob('/home/kilox/Database/Done/oil_fouling/images/val/*.json')
    Convert(labelme_json, 'cache/val.json')
