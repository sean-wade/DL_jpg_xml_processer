import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

os.remove('Annotations/desktop.ini')
xml_path = 'Annotations/'

xml_list = os.listdir(xml_path)
print(xml_list)

for f in xml_list:
    print(xml_path + f)
    tree = ET.parse(xml_path + f)
    root = tree.getroot()
    folder = root.findall('folder')
    filename = root.findall('filename')
    path = root.findall('path')
    
    folder[0].text = 'VOCdevkit'
    filename[0].text = f[:-4]
    path[0].text = 'VOCdevkit/VOC2007/JPEGImages/'+f.replace('.xml', '.jpg')
    
    tree.write(xml_path + f)

        
    

            


