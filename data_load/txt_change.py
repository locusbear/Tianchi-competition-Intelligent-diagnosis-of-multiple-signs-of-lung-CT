#coding:utf-8
#更换四个坐标的顺序，x1 y1 x2 y2变成了 x1 x2 y1 y2.（后续使用的voc2007数据集的转换也是使用的这种格式。）
from __future__ import division
 
with open(r'/home/zkpk/devdata/cmy/faster_rcnn/code/726.txt','r') as f1:
    lines = f1.readlines()#读取文本每一行
len(lines)
list = []
f2 = open("/home/zkpk/devdata/cmy/faster_rcnn/code/828.txt", "w")
for i in range(len(lines)):
    list.append(lines[i])#将每一行的数据加入列表
    clip_name = list[i].split(',')[2]
    #one=list[i].split(',')[4]
    #one = clip_name.split('/',2)[0]
    #two=clip_name.split('/',2)[1]
    #three=clip_name.split('/',2)[2]
    #four=clip_name.split('/',2)[3]
    #five=clip_name.split('/')[3]
    #six=clip_name.split('/')[7]
    #siven=list[i].split('.')[0][-3:]
    #print(siven)
    clip = list[i].split(',')[0]
    movie_name = list[i].split(',')[1]#视频名称
    #start = list[i].split(',')[2]#开始帧数
    end = list[i].split(',')[3]#结束帧数
    query = list[i].split(',')[4]#query句子
    six6=list[i].split(',')[5]
    #one=str(/home/zkpk/devdata)
    #two=str(/cmy)
    #three=str(/faster_rcnn)
    #four=str(/part1)
    #将视频帧数换算成时间，帧率是29.4fps
    #s = format(int(start)/(29.4),'.1f')
    #e = format(int(end)/(29.4),'.1f')
    clip_query = clip+','+movie_name+','+end+','+clip_name+','+query+','+six6
    #写入新建的空白文本中
    f2.write(clip_query)
