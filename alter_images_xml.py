import cv2
import sys
import os
import xml.etree.ElementTree as ET
import glob

#xml_path = sys.argv[1]
#images_path = sys.argv[2]
xml_path = 'Annotations/'
images_path = 'JPEGImages/'

files = glob.glob(xml_path+'/*.xml')
error_files = []
for xml_file in files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    xml_width = int(root.find('size')[0].text)
    xml_height = int(root.find('size')[1].text)
    xml_name = xml_file.split('/')[-1].split('.')[0]
    exts = ['jpg','JPG','png','jpeg']
    for ext in exts:    
        image_name = os.path.join(images_path+'{}.'.format(xml_name)+ext)
        image = cv2.imread(image_name)
        if image is not None:
            img_height = image.shape[0]
            img_width = image.shape[1]
            if xml_width == 0 or xml_height == 0:
                error_files.append(xml_file)
                cv2.imwrite(image_name,image)
                image_change = cv2.imread(image_name)
                root.find('size')[0].text = str(img_width) 
                root.find('size')[1].text = str(img_height) 
                tree.write(xml_file)
            elif img_width != xml_width or img_height != xml_height:
                error_files.append(xml_file)
                transposed_image = cv2.transpose(image)
                fliped_image_x = cv2.flip(transposed_image,0)
                cv2.imwrite(image_name,fliped_image_x)
print('number of images and xml_files modeified:',len(error_files))
