#!/usr/bin/python
# -*- coding: UTF-8 -*-
import review_result


if __name__ == '__main__':
     opt = review_result.ReviewInput()
     review = review_result.Reviewer()
     review.review(opt)

'''
1,26_bpmh_15.jpg,bj_bpmh,0.9999535,373,357,2127,1762
2,14_bpmh_2.jpg,bj_bpmh,0.9995017,588,368,968,746
3,16_bpmh_13.jpg,bj_bpmh,0.9998815,2213,1454,3032,2367
4,yw_nc_699.jpg,bj_bpmh,0.85246956,185,132,471,422
29_bjps_136.jpg
26_bpmh_15.jpg
14_bpmh_2.jpg
16_bpmh_13.jpg
yw_nc_699.jpg
'''