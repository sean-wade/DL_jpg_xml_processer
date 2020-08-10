import sys
import os
from tqdm import tqdm

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


root = 'Annotations/'

split = 'train'

xml_list = []
lines = open('ImageSets/Main/'+split+'.txt', 'r').readlines()
for line in lines:
    xml_list.append(line.rstrip() + '.xml')

cates = []
cate_count = {}
num = 0

for f in tqdm(xml_list):
        tree = ET.parse(root + f)
        anno = tree.getroot()
        for chd in anno.iter():
            if chd.tag == 'name':      
                cates.append(chd.text)
                #print(chd.text)
                num += 1
        tree.write(root + f)


cate_set = set(cates)
print(cate_set)
with open('cate_set_'+split+'.txt', 'a') as t:
    for c in cate_set:
        t.write("'" + c + "'," + '\n')



for item in cate_set:
    cate_count[item] = cates.count(item)

print(cate_count)
with open('cate_count_'+split+'.txt', 'a') as t:
    for k,v in cate_count.items():
        t.write("'"+str(k)+"'"+':'+"'"+str(v)+"'"+',\n')

