# DL_jpg_xml_processer
Scripts to process the jpg and xml using for deeplearning......


1、alter_images_xml.py：
    旋转一些opencv打开与labelImg标注文件有90度差异的图片
    
2、bad_xml.py  &&  delete_bad_xml.py
    打印 && 删除无法打开的xml文件

3、delete_trees_part.py
    删除所有xml标注文件中，不在列表中的标签
    注意：会对xml文件永久修改，一定要备份

4、different.py 
    比较Annotations与JPEGImages下面的文件差异
    
5、G_name.py
    重命名文件夹下的所有文件

6、makeVocTxt.py
    按比例制作VOC需要的txt（train、test、val）

7、remove_txt_line.py
    从txt中移除另一个txt出现的所有内容（按行读取）
    
8、xml_cates.py  &&  xml_cates_txt.py
    获取  （Annotations文件夹下）  &&  （split(如train).txt下）  所有xml文件中的label集合与数量（排序）
    结果保存在cate_set.txt与cate_count.txt下
    
9、xml_no_box.py
    获取文件夹中没有objects的xml文件（一般在执行删除标签后会出现）
    
10、xml_rename_label.py
    重命名一些错误label标签名称
    
11、xml_wh_0.py
    获取标注矩形框宽度、高度是0的xml文件
    
