import sys
import os

try:
    import xml.etree.cElementTree as ET
    from xml.etree.cElementTree import Element
except ImportError:
    import xml.etree.ElementTree as ET
    from xml.etree.ElementTree import Element


path = 'label/'

xml_list = os.listdir(path)


for f in xml_list:
    tree = ET.parse(path + f)
    root = tree.getroot()
    anno = root.get("annotation")

    
    #创建一级目录
    #element = Element('train',{'name':'wang'}) #指点里面是属性，结果展示：<train name="wang">
    element = Element('filename')
    element.text = '%s.jpg'%(f.split('.')[0])
    #创建二级目录
    #one=Element('id')
    '''结果展示：
    <train name="wang">
        <id>1</id>
    </train>'''
    #one.text='1'#二级目录的值 #结果展示：<id>1</id>
    #element.append(one)#将二级目录加到一级目录里
    #将一级目录加到根目录里
    root.append(element)    
    
    #让结果保存进文件就可以了
    tree.write(path + f)
