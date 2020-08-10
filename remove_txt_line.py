import sys
import os

split = 'val'

root = 'ImageSets/Main/'
txt = root+split+'.txt'

with open(txt, 'r') as t:
    lines = t.readlines()   
txt_rm = 'no_box.txt'
with open(txt_rm, 'r') as t:
    lines_rm = t.readlines()  
print(len(lines))
for rm in lines_rm:
    if rm in lines:
        print(rm)
        lines.remove(rm)  
print(len(lines))
new_txt = open(split+'_new.txt', 'a')
for xml in lines:
    new_txt.write(xml)
