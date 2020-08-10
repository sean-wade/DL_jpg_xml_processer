import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


path = 'Annotations/'

xml_list = os.listdir(path)


for f in xml_list:
    tree = ET.parse(path + f)
    root = tree.getroot()
    objects = root.findall('object')
    for obj in objects:
        name = obj.find('name').text
        
        if name == 'bj_bjmh':
            print(name, f)
            obj[0].text = 'bj_bpmh'
            tree.write(path + f)
        if name == 'bj_bpps':
            print(name, f)
            obj[0].text = 'bj_bjps'
            tree.write(path + f)

        if name == 'jyzps':
            print(name, f)
            obj[0].text = 'jyz_ps'
            tree.write(path + f)
        
    

            


