#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import xml.dom.minidom as minidom
import numpy as np
import metrics


class ReviewInput:
    result_list = "/home/kilox/save.txt"
    iou_thres = 0.4
    conf_thresh = 0.01
    gt_path = "/home/kilox/gt.txt"
    image_dir = "/home/kilox/KiloX/kiloxp/data/test_data/detect"
    type = str(10002)

class Reviewer:

    def get_data_from_tag(self, node, tag):
        return node.getElementsByTagName(tag)[0].childNodes[0].data

    def bb_intersection_over_union(self, boxA, boxB):
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # compute the area of intersection rectangle
        interArea = (xB - xA + 1) * (yB - yA + 1)

        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)

        return iou

    def review(self, opt):
        print("Opening result list from {}".format(opt.result_list))
        with open(opt.result_list) as f:
            result_file = [x.strip() for x in f]
        # assert len(result_file) >=1, 'check result file'

        file_path = opt.gt_path
        print("Opening gt list from {}".format(file_path))
        with open(file_path) as f:
            gt_file = [x.strip() for x in f]
        # assert len(result_file) >=1, 'check ground truth file'

        thres = opt.conf_thresh
        iou_thres = opt.iou_thres
        gt_count, pred_count, hit_count = {}, {}, {}
        result_dict = {}

        scores, labels = {}, {}

        # Parsing result list
        for idx, line in enumerate(result_file):
            # Skip header
            if idx > 0:
                ID, result_img_name, cls_idx, score, bbox_x1, bbox_y1, bbox_x2, bbox_y2 = line.split(",")
                score = float(score)
                bbox_x1 = int(float(bbox_x1))
                bbox_y1 = int(float(bbox_y1))
                bbox_x2 = int(float(bbox_x2))
                bbox_y2 = int(float(bbox_y2))
                result_img_name = result_img_name.split('.')[0]
                # Save results in a dict
                result_dict[result_img_name] = result_dict.get(result_img_name, [])
                result_dict[result_img_name].append([cls_idx, score, bbox_x1, bbox_y1, bbox_x2, bbox_y2])
        # print(result_dict)
        # Parsing groundtruth list

        for idx, path in enumerate(gt_file):
            img_name = path.split('.')[0]
            xml_path = os.path.join(opt.image_dir, img_name + '.xml')
            print(xml_path)
            with open(xml_path) as f:
                data = minidom.parseString(f.read())
            objs = data.getElementsByTagName("object")
            num_objs = len(objs)
            boxes = np.zeros((num_objs, 4), dtype=np.uint16)
            gt_classes = [""] * num_objs
            for ix, obj in enumerate(objs):
                x1 = float(self.get_data_from_tag(obj, "xmin"))
                y1 = float(self.get_data_from_tag(obj, "ymin"))
                x2 = float(self.get_data_from_tag(obj, "xmax"))
                y2 = float(self.get_data_from_tag(obj, "ymax"))
                cls_idx = str(self.get_data_from_tag(obj, "name")).lower().strip()
                boxes[ix, :] = [x1, y1, x2, y2]
                gt_classes[ix] = cls_idx
                gt_count[cls_idx] = gt_count.get(cls_idx, 0) + 1
            flag = {}
            for gt_box in boxes:
                flag[str(gt_box.tolist())] = 0
            # Compare prediction result with groundtruth
            if img_name in result_dict:
                results = result_dict[img_name]
                for result in results:
                    cls_idx, score, bbox_x1, bbox_y1, bbox_x2, bbox_y2 = result
                    pred_box = [bbox_x1, bbox_y1, bbox_x2, bbox_y2]
                    # import pdb;pdb.set_trace()
                    # Thresholding
                    if score >= thres:
                        pred_count[cls_idx] = pred_count.get(cls_idx, 0) + 1

                        ####################################
                        score_list = scores.get(cls_idx, [])
                        score_list.append(score)
                        scores[cls_idx] = score_list
                        is_hit = False
                        hit_cls = cls_idx
                        ####################################
                        for gt_box, gt_cls in zip(boxes, gt_classes):
                            iou = self.bb_intersection_over_union(pred_box, gt_box.tolist())
                            if iou >= iou_thres and cls_idx == gt_cls:
                                if flag[str(gt_box.tolist())] == 0:
                                    hit_count[gt_cls] = hit_count.get(gt_cls, 0) + 1
                                    flag[str(gt_box.tolist())] = 1
                                    ####################################
                                    is_hit = True
                                    hit_cls = gt_cls
                        if is_hit:
                            labels_list = labels.get(hit_cls, [])
                            labels_list.append(True)
                            labels[hit_cls] = labels_list
                        else:
                            labels_list = labels.get(hit_cls, [])
                            labels_list.append(False)
                            labels[hit_cls] = labels_list
                        ####################################
                # print hit_count, result, boxes

        print("gt_count:{}\n pred_count:{}\n hit_count:{}".format(gt_count, pred_count, hit_count))

        mAP = 0.0
        prec, rec, AP = {}, {}, {}
        for key, value in pred_count.items():
            prec[key] = hit_count[key] / float(value)
            rec[key] = hit_count[key] / float(gt_count[key])
            print("For class {} with conf_thresh:{}, precision:{:4f} recall:{:4f} " \
                  .format(key, thres, prec[key], rec[key]))

            #############################
            np_scores = np.asarray(scores[key])
            np_labels = np.asarray(labels[key])
            metrics_prec, metrics_rec = metrics.compute_precision_recall(np_scores, np_labels, gt_count[key])
            AP[key] = metrics.compute_average_precision(metrics_prec, metrics_rec)
            mAP += AP[key]
            print("For class {}: ap:{:4f}".format(key, AP[key]))

            print("For class {} Score = {} \n".format(key, AP[key] * 0.5 + rec[key] * 0.3 + prec[key] * 0.2))
            ############################

        key_out = opt.type
        # assert key_out in rec, 'there is no such type in the image'
        # save_file_name = opt.result_list.split('/')[-1].split('.')[0] + "_" + key_out + "_result.ini"
        # print(save_file_name)
        with open("/home/kilox/result.txt", "w") as output:
            output.write("AP=" + str(AP[key_out]) + "\n")
            output.write("R=" + str(rec[key_out]) + "\n")
            output.write("P=" + str(prec[key_out]) + "\n")
            output.write("IoU=" + str(iou_thres) + "\n")
            output.write("miss_rate=" + str(1 - rec[key_out]) + "\n")
            output.write("error_rate=" + str(1 - prec[key_out]) + "\n")
            output.write("score=" + str(AP[key_out] * 0.5 + rec[key_out] * 0.3 + prec[key_out] * 0.2) + "\n")
