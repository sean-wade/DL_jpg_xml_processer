#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run a YOLO_v3 style detection model on test images.
"""

import colorsys
import os
from timeit import default_timer as timer
import time
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2
import piexif

traindata_path = 'JPEGImages'
num_count = 0
for img in os.listdir(traindata_path):
    try:
        image = Image.open(traindata_path + '/' + img)
        piexif.remove(traindata_path + '/' + img)
        # print("单幅图像", image.mode)
    except:
        print(img)
        os.remove(traindata_path + '/' + img)
        print('Open Error! Try again!')

