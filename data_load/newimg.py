#coding:utf-8
import cv2
import os 
import numpy as np 

#这是给给图像重命名，与voc2007的命名形式一样。比如:000000.png。不过貌似不是必须的，不换名字也可以。

with open(r'/home/zkpk/devdata/cmy/faster_rcnn/code/2.txt','r') as f1:
    lines = f1.readlines()#读取文本每一行
#len(lines)
lists = []
dst=[]
#f2 = open("/home/zkpk/devdata/cmy/faster_rcnn/code/828.txt", "w")
for i in range(len(lines)):
    lists.append(lines[i])#将每一行的数据加入列表
    clip_name = lists[i].split(',')[0]
    one=clip_name.split('/')[8]
    #print(one)
    two=clip_name.split('/')[7]
    dst.append(two)
    #nums=set(dst)
    #nums=len(nums)
    #print(nums)
    #return
    #print(clip_name)
    #one=list[i].split(',')[4]
    #one = clip_name.split('/',2)[0]
    #two=clip_name.split('/',2)[1]
    #three=clip_name.split('/',2)[2]
    #four=clip_name.split('/',2)[3]
    #five=clip_name.split('/')[3]
    #six=clip_name.split('/')[7]
    #siven=list[i].split('.')[0][-3:]
    #print(siven)
    #clip = list[i].split(',')[0]
    #movie_name = list[i].split(',')[1]#视频名称
    #start = list[i].split(',')[2]#开始帧数
    #end = list[i].split(',')[3]#结束帧数
    #query = list[i].split(',')[4]#query句子
    #six6=list[i].split(',')[5]
    #one=str(/home/zkpk/devdata)
    #two=str(/cmy)
    #three=str(/faster_rcnn)
    #four=str(/part1)
    #将视频帧数换算成时间，帧率是29.4fps
    #s = format(int(start)/(29.4),'.1f')
    #e = format(int(end)/(29.4),'.1f')
    #clip_query = clip+','+movie_name+','+end+','+clip_name+','+query+','+six6
    #写入新建的空白文本中
    #f2.write(clip_query)
dst.sort()
dic={}
nums=set(dst)
nums=list(nums)
nums.sort()
for index,values in enumerate(nums):
    dic[values]=index
#print(dic["628127"])



#print(nums)
#print(len(nums))

lis=[]
ll=[]

for i in range(len(lines)):
    #print(i)
    lis.append(lines[i])#将每一行的数据加入列表
    png_name = lis[i].split(',')[0]
    one=png_name.split('/')[8]
    two=png_name.split('/')[7]
    exc_png=one[:-4]
    if two in dic:
        #print(two)
        #print(dic[two])
        if len(str(dic[two]))==1:
            #print(str(dic[two]))
            newname=str(000)+str(dic[two])+exc_png
            #print(newname)
            newname=str(0)+newname
            new_path='/home/zkpk/devdata/cmy/faster_rcnn/pngimg/'+str(newname)+'.png'
            #new_img=cv2.imread(png_name)
            #new_save_img=cv2.imwrite(new_path,new_img)


        elif len(str(dic[two]))==2:
            newname=str(0)+str(dic[two])+exc_png
            new_path='/home/zkpk/devdata/cmy/faster_rcnn/pngimg/'+str(newname)+'.png'
            #print(newname)
            #ll.append(newname)
            new_img=cv2.imread(png_name)
            new_save_img=cv2.imwrite(new_path,new_img)
        else:
            newname=str(dic[two])+exc_png
            #print(newname)
            new_path='/home/zkpk/devdata/cmy/faster_rcnn/pngimg/'+str(newname)+'.png'
            #ll.append(newname)
            new_img=cv2.imread(png_name)
            new_save_img=cv2.imwrite(new_path,new_img)
    #img=cv2.imread(png_name)
    #new_path='/home/zkpk/devdata/cmy/faster_rcnn/pngimg/'+
    #newimg=cv2.imwrite()
#print(ll)
