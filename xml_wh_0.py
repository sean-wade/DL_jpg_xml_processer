import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


path = '../../VOCdevkit/VOC2007/Annotations/'

xml_list = os.listdir(path)


for f in xml_list:
    tree = ET.parse(path + f)
    root = tree.getroot()
    size = root.find('size')
    width = size.find('width').text
    height = size.find('height').text
    if int(width) ==0 or int(height) == 0:
        print(f)
        fname = f.split('.')[0]
        jpg_name = 'JPEGImages/'+fname+'.jpg'
        if os.path.exists(jpg_name):
            os.remove('JPEGImages/'+fname+'.jpg')

    

