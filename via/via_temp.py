import json
import os
import re

filename = '/home/kilox/Database/Raw/Visual/Image/kilox_outdoor_20190927/via_project_27Sep2019_13h43m.json'
image_dir = "/home/kilox/Database/Raw/Visual/Image/kilox_outdoor_20190927/templa"

file_list = os.listdir(image_dir)

with open(filename) as f:
    master_dicts = json.load(f)

image_metadata_dict = master_dicts["_via_img_metadata"]

for item in file_list:
    for it in image_metadata_dict:
        if re.match(item, it) != None:
            item_dict = image_metadata_dict[it]
            regions_list = item_dict["regions"]
            id_str = item[:-4]
            id = int(id_str)

            scale_points = []
            scale_numbers = []
            for it_region_dict in regions_list:
                # print(it_region_dict["shape_attributes"])
                shape_attributes_dict = it_region_dict["shape_attributes"]
                if shape_attributes_dict["name"] == "point":
                    cx = shape_attributes_dict["cx"]
                    cy = shape_attributes_dict["cy"]
                    scale_points.append(cx)
                    scale_points.append(cy)
                    scale_number = it_region_dict["region_attributes"]["name"]
                    scale_numbers.append(scale_number)

                if shape_attributes_dict["name"] == "rect":
                    x = shape_attributes_dict["x"]
                    y = shape_attributes_dict["y"]
                    width = int(shape_attributes_dict["width"]) + int(x)
                    height = int(shape_attributes_dict["height"]) +int(y)
                    bbox = [x, y, width, height]

            write_item_dict = {"part_info_list": [{"id": id, "bbox": bbox, "corners": '0', "digit_num": 0,
                                                   "scale_points": scale_points, "scale_numbers": scale_numbers,
                                                   "precision": 2}]}
            with open(image_dir+'/' + item[:-4] + '.json', 'w') as f:
                json.dump(write_item_dict, f)
