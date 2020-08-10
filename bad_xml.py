import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


root = '../../VOCdevkit/VOC2007/Annotations/'

xml_list = os.listdir(root)


count_good = 0
count_bad = 0
with open('bad_xml.txt', 'a') as t:
    for f in xml_list:
        try:
            anno = ET.parse(root + f).getroot()
            count_good += 1
        except ET.ParseError:
            print('Bad file: ', f)
            count_bad += 1
            t.write(f + '\n')

            

print('count_good: ', count_good)
print('count_bad: ', count_bad)

