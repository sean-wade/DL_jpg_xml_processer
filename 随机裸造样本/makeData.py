import cv2
import random
import numpy as np
from xml_helper import generate_xml
import os
from skimage import exposure

def jitter(box):
    #if random.random() < 0.3:
    #    box = cv2.cvtColor(box, cv2.COLOR_BGR2RGB)
    if random.random() < 0.5:
        box = cv2.flip(box, 1)
    if random.random() < 0.3:
        box = cv2.flip(box, 0)
    flag = random.uniform(0.2, 1.8) #flag>1为调暗,小于1为调亮
    box = exposure.adjust_gamma(box, flag)
    return box


def put(box, pano, label = 'yw_nc'):
    #randsize = random.randint(2, 10) / 10.
    new_w = random.randint(80, 300)
    new_h = int(new_w / box.shape[1] * box.shape[0])
    #print(randsize)
    #new_h, new_w = int(box.shape[0] * randsize), int(box.shape[1] * randsize)
    box = cv2.resize(box, (new_w, new_h))
    
    box = jitter(box)
    
    pano_h, pano_w = pano.shape[0], pano.shape[1]
    rand_x, rand_y = random.randint(0, pano_w - new_w), random.randint(0, pano_h - new_h)
    for i in range(new_w - 1):
        for j in range(new_h - 1):
            if np.mean(box[j, i]) < 250:
                pano[rand_y+j, rand_x+i] = box[j, i]
    return pano, [rand_x, rand_y, rand_x+new_w, rand_y+new_h, label]
    #[[x_min, y_min, x_max, y_max, name]]


def annot(obj_path, img_path):
    box  = cv2.imread('obj/' + obj_path)
    pano = cv2.imread('img/' + img_path)
    coords = []
    for i in range(random.randint(1, 2)):
        pano, coord = put(box, pano)
        coords.append(coord)
    cv2.imwrite('generate/' + img_path, pano)
    generate_xml(img_path, coords, list(pano.shape), 'generate/')


objs = os.listdir('obj/')
imgs = os.listdir('img/')

for img in imgs:
    obj_idx = random.randint(0, len(objs) - 1)
    print(objs[obj_idx], img)
    annot(objs[obj_idx], img)



