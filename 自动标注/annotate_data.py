# 自动标注图片 #

import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
from PIL import Image
from xml_helper import *

# 初始化参数
confThreshold = 0.4  # 置信度阈值
nmsThreshold = 0.5  # NMS阈值
inpWidth = 608       # 网络输入图像宽
inpHeight = 608      # 网络输入图像高

# 加载标签名称
classesFile = "cfg/voc.names" # 标签文件的路径
classes = None
# 将voc.names文件中的标签名称放入classes变量中
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n') 

modelConfiguration = "cfg/yolov3-voc.cfg" # 配置文件的路径
modelWeights = "cfg/yolov3-voc.backup" # 模型权重的路径

# 从磁盘加载YOLO文件后利用OpenCV中的cv2.dnn.readNetFromDarknet函数从中读取网络结构及权重参数，此函数需要两个参数configPath 和 weightsPath
net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
# 读取网络之后设置DNN后端为OpenCV，参数为后台计算ID，-DNN_BACKEND_INFERENCE_ENGINE表示使用intel的预测推断库（安装了OpenVINO才能使用）；-DNN_BACKEND_OPENCV 一般情况都是使用opencv dnn作为后台计算

net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)

# DNN的目标设置，参数：-DNN_TARGET_CPU 在CPU设备上使用；-DNN_TARGET_OPENCL 在GPU上运行
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU) 


def getOutputsNames(net):
    '''
    描述：获取网路最后一层
    net:网络
    输出：输出层
    '''
    # 获取所有层的名称
    layersNames = net.getLayerNames()
    # 返回最后一层；getUnconnectedOutLayers()函数给出了未连接的输出层名称
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def drawPred(classId, conf, left, top, right, bottom):
    '''
    描述：根据检测的信息在图片上画框并保存图片
    输入：标签索引，置信度，左上角x，左上角y，右下角x，右下角y
    '''
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    label = '%.2f' % conf
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)


def postprocess(frame, outs):
    '''
    描述：将网络最后一层的信息取出，网络 bounding boxes 每个输出都由一组`5 + 类数目`个元素的向量表示。前4个元素代表`center_x，center_y，width，height`。第五个元素表示边界框包围对象的置信度。其余元素是与每个类相关的置信度（即对象类型）。该框被分配到与该框的最高分相对应的那一类。
    输入：图片，网落最后一层
    输出：[xmin,ymin,xmax,ymax,class]
    '''
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    
    classIds = [] # 检测到的对象的类标签
    confidences = [] # YOLO分配给对象的置信度值
    boxes = [] # YOLO检测得到的对象的边界框
    coords = [] # 对象边界框的坐标和标签，[xmin,ymin,xmax,ymax,label]
    ## 返回内容
    obj=list()
    for out in outs:
        for detection in out:
            scores = detection[5:]           # 分数
            classId = np.argmax(scores)      # 分类索引
            confidence = scores[classId]     # 置信度
            if confidence > confThreshold:    # 如果置信度大于阈值，取数据
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
                objc= classes[classId]+','+str(confidence)+','+str(left)+','+str(top)+','+str(width)+','+str(height)
                obj.append(objc)
    #print(obj)
    # 利用OpenCV内置的NMS DNN模块实现非最大值抑制 ，所需要的参数是边界框、置信度、以及置信度阈值和NMS阈值。
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        #drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
        coord = [left, top, left + width, top + height, classes[classIds[i]]]
        coords.append(coord)
        
    # return obj
    return coords
    

img_path='/home/lm/lm_labelimgs/annotate_data/imgs' # 需要自动标注图片的路径
image=os.listdir(img_path)


for i in range(len(image)):
    
    imgpath = os.path.join(img_path,image[i])
    print(imgpath)
    cap = cv.VideoCapture(imgpath)
    hasFrame, frame = cap.read()
    imgsize=list(frame.shape)
    
    # 将Image转换成blob格式
    blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

    # 输入图片进网络模型
    net.setInput(blob)

    # 运行前向网络，获得前向传播的结果，OpenCV的网络类中的前向功能需要结束层，参数（输出层名）
    outs = net.forward(getOutputsNames(net))
    
    # 后处理网络输出，得到坐标和标签
    coords = postprocess(frame, outs)
   
    # 存放自动标注完生成的.xml路径
    xml_savepath ='/home/lm/lm_labelimgs/annotate_data/xmls'  

    # 生成.xml文件，[图片名，坐标+标签，图像尺寸，.xml路径]
    generate_xml(str(image[i]), coords, imgsize, xml_savepath)

print('done')




