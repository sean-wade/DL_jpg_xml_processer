# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:27:19 2020
@author: gonglei
describetion: 用于voc格式的数据集，对其中各类别的图片数量，标注数量，最小宽高，最大宽高，最小宽高占比，最大宽高占比进行统计
              根据统计结果生成数据的统计图表
"""

import os
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def GetAnnotBoxLoc(AnotPath):             #AnotPath VOC标注文件路径
    tree = ET.ElementTree(file=AnotPath)  #打开文件，解析成一棵树型结构
    root = tree.getroot()                 #获取树型结构的根
    SizeSet = root.findall('size')
    width   = int(SizeSet[0].find('width').text)
    height  = int(SizeSet[0].find('height').text)
    ObjectSet = root.findall('object')      #找到文件中所有含有object关键字的地方，这些地方含有标注目标
    ObjBndBoxSet = {}                       #以目标类别为关键字，目标框为值组成的字典结构
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox  = Object.find('bndbox')
        x1 = int(BndBox.find('xmin').text)
        y1 = int(BndBox.find('ymin').text)
        x2 = int(BndBox.find('xmax').text)
        y2 = int(BndBox.find('ymax').text)
        BndBoxLoc = [x1,y1,x2,y2]
        if ObjName in ObjBndBoxSet:
            ObjBndBoxSet[ObjName].append(BndBoxLoc)#如果字典结构中含有这个类别了，那么这个目标框要追加到其值的末尾
        else:
            ObjBndBoxSet[ObjName] = [BndBoxLoc]      #如果字典结构中没有这个类别，那么这个目标框就直接赋值给其值吧
    return ObjBndBoxSet, [width, height]


def CountData(path_imgs, path_labels):
    # files_imgs   = os.listdir(path_imgs)
    files_labels = os.listdir(path_labels)
    statistics = {}

    for i in tqdm(range(len(files_labels))):
        # path_img   = os.path.join(path_imgs, files_labels[i][0:-3]+'jpg')
        path_label = os.path.join(path_labels, files_labels[i])
        try:
            labels, size = GetAnnotBoxLoc(path_label)
            for key in labels:
                w_min = min([box[2]-box[0] for box in labels[key]])
                h_min = min([box[3]-box[1] for box in labels[key]])
                w_max = max([box[2]-box[0] for box in labels[key]])
                h_max = max([box[3]-box[1] for box in labels[key]])
                w_min_r = round(w_min/size[0],3)
                h_min_r = round(h_min/size[1],3)
                w_max_r = round(w_max/size[0],3)
                h_max_r = round(h_max/size[1],3)
                if key not in statistics:
                    # 图片数量，标签数量, 最小宽高，最大宽高， 最小宽高占比， 最大宽高占比
                    statistics[key] = [1, len(labels[key]), w_min, h_min, w_max, h_max, w_min_r, h_min_r, w_max_r, h_max_r]
                else:
                    statistics[key][0] += 1
                    statistics[key][1] += len(labels[key])
                    statistics[key][2] = w_min if w_min < statistics[key][2] else statistics[key][2]
                    statistics[key][3] = h_min if h_min < statistics[key][3] else statistics[key][3]
                    statistics[key][4] = w_max if w_max > statistics[key][4] else statistics[key][4]
                    statistics[key][5] = h_max if h_max > statistics[key][5] else statistics[key][5]
                    statistics[key][6] = w_min_r if w_min_r < statistics[key][6] else statistics[key][6]
                    statistics[key][7] = h_min_r if h_min_r < statistics[key][7] else statistics[key][7]
                    statistics[key][8] = w_max_r if w_max_r > statistics[key][8] else statistics[key][8]
                    statistics[key][9] = h_max_r if h_max_r > statistics[key][9] else statistics[key][9]
        except:
            with open('error.txt','a') as f:
                f.write(path_label + '\n')

    return statistics


def VisualData(statistics):
    ''' 绘制各类别图片数量和标注数量柱状图，并按照降序排列'''

    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
    # 绘制图片数量柱状图
    statistics_order_imgnum=sorted(statistics.items(),key=lambda x:x[1][0],reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。x相当于字典集合中遍历出来的一个元组
    plt.figure()
    rects = plt.bar([cont[0] for cont in statistics_order_imgnum], [cont[1][0] for cont in statistics_order_imgnum])
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=7, ha='center', va='bottom', rotation=-90)

    plt.xlabel('类别',FontProperties=font)
    plt.xticks(rotation=-90)
    plt.ylabel('数量',FontProperties=font)
    plt.title('各类别图片数量统计',FontProperties=font)
    plt.tight_layout()
    plt.savefig("各类别图片数量统计.png",dpi=500,bbox_inches = 'tight')
    plt.show()

    # 绘制标注数量柱状图
    statistics_order_labelnum=sorted(statistics.items(),key=lambda x:x[1][1],reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。x相当于字典集合中遍历出来的一个元组
    plt.figure()
    rects = plt.bar([cont[0] for cont in statistics_order_labelnum], [cont[1][1] for cont in statistics_order_labelnum])
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=7, ha='center', va='bottom', rotation=-90)

    plt.xlabel('类别',FontProperties=font)
    plt.xticks(rotation=-90)
    plt.ylabel('数量',FontProperties=font)
    plt.title('各类别标注数量统计',FontProperties=font)
    plt.tight_layout()
    plt.savefig("各类别标注数量统计.png",dpi=500,bbox_inches = 'tight')
    plt.show()


def VisualDataSize(path_imgs, path_labels):
    ''' 绘制数据集中所有标注的尺度分布，统一到255*255分辨率下'''

    files_labels = os.listdir(path_labels)
    size_wh = {}

    for i in tqdm(range(len(files_labels))):
        path_label = os.path.join(path_labels, files_labels[i])
        try:
            labels, size = GetAnnotBoxLoc(path_label)
            for key in labels:
                wh_yolo = ([[(box[2]-box[0])/size[0], (box[3]-box[1])/size[1]] for box in labels[key]])
                if key not in size_wh:
                    size_wh[key] = []
                    for wh in wh_yolo:
                        size_wh[key].append(wh)
                else:
                    for wh in wh_yolo:
                        size_wh[key].append(wh)
        except:
            with open('error.txt','a') as f:
                f.write(path_label + '\n')

    # 将各个标注的宽高全部统一到0-99，并在图像上显示，以观察数据整体尺度分布
    img = Image.new('I', (256, 256))
    img_a = np.array(img)
    for key in size_wh:
        for wh in size_wh[key]:
            x = int(wh[0]*255)
            y = int(255-wh[1]*255)
            img_a[y,x] += 1
    val_max = img_a.max()
    img_a = (img_a/val_max)**0.5*255 # 修改映射方式，便于观察
    img = Image.fromarray(img_a.astype('uint8')).convert('L')
    plt.imshow(img, cmap=plt.cm.gray)
    img.save('数据集尺度分布.png')




path_imgs = "D:\\Data\\缺陷检测\\gw\\JPEGImages\\"
path_labels = "D:\\Data\\Detection\\defect\\ori\\Annotations\\"
statistics = CountData(path_imgs, path_labels)
VisualData(statistics)
VisualDataSize(path_imgs, path_labels)

with open('statistics.txt','a') as f:
    for key in statistics:
        f.write(key + ' ' + str(statistics[key][0]) + ' ' + str(statistics[key][1]) + ' ' +
                str(statistics[key][2]) + ' ' + str(statistics[key][3]) + ' ' +
                str(statistics[key][4]) + ' ' + str(statistics[key][5]) + ' ' +
                str(statistics[key][6]) + ' ' + str(statistics[key][7]) + ' ' +
                str(statistics[key][8]) + ' ' + str(statistics[key][9]) + ' ' +'\n')







