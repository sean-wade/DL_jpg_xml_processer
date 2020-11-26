# -*- coding:utf-8 -*-
# @Time: 下午7:23
# @Author:lm
# @File:PIL_rotate.py
# @Software:PyCharm


import os
import piexif
import numpy as np
from PIL import Image, ExifTags, ImageOps


def load_image_file(image_file):
    # 加载图片为PIL格式
    image = Image.open(image_file)

    # 先判断图片是否有exif_transpose属性
    # hasattr()函数用于判断对象是否包含对应的属性
    if hasattr(image, "_getexif"):
        # 获取图片exif信息
        exif_data = image._getexif()
        if exif_data is not None:
            # 处理exif转换
            image = exif_transpose(image)
        else:
            image = image

    return image


def exif_transpose(image):

    if not image:
        return image

    exif_orientation_tag = 274
    # 获取图片exif信息
    exif_data = image._getexif()

    # 对象exif信息是否为空，exif_data数据类型是否为字典类型，exif_data里是否包含方向标签。
    if isinstance(exif_data, dict) and exif_orientation_tag in exif_data:
        # 获取方向信息
        orientation = exif_data[exif_orientation_tag]
        # 处理EXIF方向
        if orientation == 1:
            # 正常图片
            pass
        elif orientation == 2:
            # 从左到右镜像
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # 逆时针旋转180度
            image = image.rotate(180, expand=True)
        elif orientation == 4:
            # 从上到下的镜像
            image = image.rotate(180, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # 沿左上角镜像
            image = image.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            # 顺时针旋转90度
            image = image.rotate(-90, expand=True)
        elif orientation == 7:
            # 沿右上角镜像
            image = image.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            # 逆时针旋转90
            image = image.rotate(90, expand=True)

    return image


def unify_image_name(image_amount):
    name_len = 6
    # 计算0 的个数
    num_of_zero = name_len - len(str(image_amount))

    prefix = 'cabinet'
    edition = '02'
    new_name = prefix + '_' + edition + '_' + '0' * num_of_zero + str(image_amount) + '.jpg'
    return new_name


def main():
    data_dir = '/home/lm/VOCdevkit/Auto_Station_DataSet/BJ_subcontract/JPEGImages/'
    save_dir = '/home/lm/VOCdevkit/Auto_Station_DataSet/BJ_subcontract/EXIF_img/'
    image_list = os.listdir(data_dir)
    image_amount = 200

    for image_file in image_list:
        full_path = os.path.join(data_dir, image_file)
        image_rotate = load_image_file(full_path)

        image_amount += 1
        # new_name = unify_image_name(image_amount)
        new_path = os.path.join(save_dir, image_file)
        image_rotate.save(new_path)

    print('done')


if __name__ == "__main__":
    main()


