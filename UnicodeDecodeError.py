# -*- coding: utf-8 -*- 
import os
import tqdm
import xml.etree.ElementTree as ET

root = "/zhanghao/dataset/YW_new/VOCdevkit/VOC2007/Annotations/"
fs = os.listdir(root)

for f in tqdm.tqdm(fs):
    tree = ET.parse(root + f)
    tree.write(root + f)
