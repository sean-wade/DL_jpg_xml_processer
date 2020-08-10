import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#from tqdm import tqdm

root = './Annotations/'

xml_list = os.listdir(root)


cates = []
cate_count = {}
num = 0

for f in (xml_list):
        tree = ET.parse(root + f)
        anno = tree.getroot()
        for chd in anno.iter():
            if chd.tag == 'name':      
                cates.append(chd.text)
                #print(chd.text)
                num += 1
        #tree.write(root + f)


cate_set = set(cates)
print(cate_set)
with open('cate_set.txt', 'a') as t:
    for c in cate_set:
        t.write("'" + c + "'," + '\n')

for item in cate_set:
    cate_count[item] = cates.count(item)
    
cate_count_sorted = sorted(cate_count.items(), key=lambda x: x[1], reverse=True)

print(cate_count_sorted)

with open('cate_count.txt', 'a') as t:
    for (k,v) in cate_count_sorted:
        t.write("{0:12}:{1:6}\n".format(str(k), str(v)))
        #t.write("'"+str(k)+"'"+':'+str(v)+',\n')

