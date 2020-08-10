import cv2
import os
#from tqdm import tqdm
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
    
xml_path = "xml/"
jpg_path = "jpg/"
file_list = os.listdir(xml_path)

if not os.path.exists("Classify/"):
    os.mkdir("Classify/")

box_n = 0
for f in (file_list):
    tree = ET.parse(xml_path + f)
    root = tree.getroot()
    objs = root.findall('object')

    if len(objs)==0:
        continue
    
    jpg = cv2.imread(jpg_path + f.split('.')[0] + '.jpg')
    if jpg is None:
        continue
    
    for obj in objs:
        if obj is None:
            continue
        
        #print(f)
        label=obj.find('name').text
        if not os.path.exists("Classify/"+label):
            os.mkdir("Classify/"+label)
            
        bbox = obj.find('bndbox')
        if bbox is None:
            continue
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        
        box_n += 1
        cut = jpg[ymin:ymax, xmin:xmax]
        cv2.imwrite("Classify/"+label+'/%d.jpg'%box_n, cut)
    