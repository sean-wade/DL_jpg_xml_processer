# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import os
prelabels=['xy',
'yxcr',
'ybh',
'ywzt_yfyc', 
'ybf', 
'jyz_lw', 
'gbps',
'bj_wkps', 
'hxq_gjtps', 
'bjdsyc', 
'wcaqm',
'wcgz', 
'gjptwss']
xml_path='/home/zjn/VOCdevkit/VOC2007/Annotations_part1'
xml_names=os.listdir(xml_path)
for name in xml_names:
    tree=ET.parse(os.path.join(xml_path,name))
    root=tree.getroot()
    objects=root.findall('object')
    for object in objects:
        #print(object)
        label=object.find('name').text
        #print(label)
        if not label in prelabels:
            #print(1)
            root.remove(object)
    tree.write(os.path.join(xml_path,name))
