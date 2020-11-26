import os
import numpy as np
import csv
import cv2
from PIL import Image
from PIL.ExifTags import TAGS


def xml_rotate_inv(orientation, wh, box):
    xmin = box[0]
    ymin = box[1]
    xmax = box[2]
    ymax = box[3]

    if orientation == 6:
        h, w = wh
        ymax1 = w - xmin
        ymin1 = w - xmax
        xmin1 = ymin
        xmax1 = ymax
    elif orientation == 3:
        w, h = wh
        xmax1 = w - xmin
        ymax1 = h - ymin
        xmin1 = w - xmax
        ymin1 = h - ymax
    elif orientation == 8:
        h, w = wh
        ymin1 = xmin
        xmax1 = h - ymin
        ymax1 = xmax
        xmin1 = h - ymax
    else:
        w, h = wh
        xmin1 = xmin
        ymin1 = ymin
        xmax1 = xmax
        ymax1 = ymax

    return [xmin1, ymin1, xmax1, ymax1]


def get_orientation(img_path):
    pil_img = Image.open(img_path)
    pil_w, pil_h = pil_img.size
    ret = {}

    try:
        info = pil_img._getexif()
    except:
        return 0, pil_w, pil_h

    if info == None:
        return 0, pil_w, pil_h

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value

    orientation = ret.get('Orientation', 'None')

    return orientation, pil_w, pil_h



img_path = '/home/ykang/4_defect_detect/test/Bj_Wild/'
savepath = '/home/ykang/4_defect_detect/test/save/'
images = os.listdir(img_path)
ROTATE_FLAG = 1


for image in images:
    imgpath =img_path + image
    try:
         
        cv2_img = cv2.imread(imgpath)
    except:
        print(imgpath)
        continue

    if cv2_img is None:
        print(imgpath)
        continue
    
    angle = -1
    if ROTATE_FLAG:
        try:
            orientation, pil_w, pil_h = get_orientation(imgpath)
            #print("angle is {} 1111111".format(orientation))
        except:
            print(imgpath)
            continue
        if orientation == 3:
            angle = 1
        elif orientation == 6:
            angle = 2
        elif orientation == 8:
            angle =0
        else:
            orientation = 0
            angle = -1
    if angle > -1:
        cv2_img_show = cv2.rotate(cv2_img, angle)
    else:
        cv2_img_show = cv2_img

    cv2.imwrite(savepath + image,cv2_img_show)


