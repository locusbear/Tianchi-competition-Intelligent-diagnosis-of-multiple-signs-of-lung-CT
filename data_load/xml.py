# ! /usr/bin/python
# -*- coding:UTF-8 -*-
import os, sys
import glob
import cv2

#这是使用网上的代码，做了一个voc2007 由 txt文件向xml转换的过程。（注意txt文件的每一行内容是 路径+x1+x2+y1+y2+class）

#src_xml_dir = '/home/zkpk/devdata/cmy/faster_rcnn/xml/'


# VEDAI 图像存储位置
src_img_dir = '/home/zkpk/devdata/cmy/faster_rcnn/pngimg/'
# VEDAI 图像的 ground truth 的 xml 文件存放位置
src_xml_dir = '/home/zkpk/devdata/cmy/faster_rcnn/xml/'


# 遍历目录读取图片
img_Lists = []
new_img_path=os.listdir(src_img_dir)
#print(len(new_img_path))
#print(new_img_path)
# for i in img_Lists:
#     print(i)

# 创建xml文件，存入图片信息

for img_item in new_img_path:
    im = cv2.imread(src_img_dir+img_item)  #打开图片 为了记录图片的长宽数据
    #print(src_img_dir+img_item)
    #img = os.path.split(img_item)[1].split('.')[0]
    img=img_item.split('.')[0]
    #print(img)
    #print(dasa)
    width, height = im.shape[0],im.shape[1]

    # write in xml file
    # os.mknod(src_xml_dir + '/' + img + '.xml')
    xml_file = open((src_xml_dir + '/' + img + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(img) + '.png' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')
    xml_file.close()

# 读取全部信息
txt_file = open('/home/zkpk/devdata/cmy/faster_rcnn/code/newxml.txt')

for line in txt_file.readlines():
    gt = line.splitlines()
    # print(gt)
#     gt = txt_file.readline().splitlines()
#     # gt = open(src_txt_dir + '/gt_' + img + '.txt').read().splitlines()

    # write the region of image on xml file
    for img_each_label in gt:
        spt = img_each_label.split(',')  # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
        #one=spt.split(',')[0]
        one=spt[0]
        ones=one[-10:-4]
        #print(ones)
        #print(dstsss)

        # 判断是否需要写入xml
        #if spt[6] == '0':
            # print (gt)

            # 打开相应xml文件
            # print(spt[5].zfill(6))
        xml_file = open((src_xml_dir + '/' +ones+ '.xml'), 'a')
        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + str(spt[5]) + '</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + str(spt[1]) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(spt[3]) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(spt[2]) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(spt[4]) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')
        xml_file.close()

# 补上结尾
xmlx=os.listdir(src_xml_dir)
#xmlx.sort()
#print(xmlx)
#print(len(xmlx))
#print(dsaaaaa)
#print(xmlx)
#print(dssrf)

for i in xmlx:
    xml_file=open((src_xml_dir + '/' +i), 'a')
    xml_file.write('</annotation>')
    xml_file.close()



'''
for i in range(4842):
    xml_file = open((src_xml_dir + '/' + str(i).zfill(6) + '.xml'), 'a')
    xml_file.write('</annotation>')
    xml_file.close()
'''