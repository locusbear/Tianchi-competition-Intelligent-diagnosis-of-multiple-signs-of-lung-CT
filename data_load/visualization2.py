import os
import sys
import numpy as np
import pandas as pd
import SimpleITK as sitk
import matplotlib.pyplot as plt
import glob
import cv2

from tqdm import tqdm

#这个代码主要的功能是使用SimpleITK读取肺部的图像，其中涉及到肺窗的概念，有阈值的相关处理。
#这个代码之前被屏蔽掉的部分做的是读取并保存图片为png格式，后来我自己又做了一个标签的保存，把路径，矩形框的四个坐标，类别保存在了一个txt文件里面。
#读取图片的时候需要注意，使用plt的话会有空白出现，我不太记得我当时是使用的cv2进行处理的，还是把空白部分给消除了。



label_dict = {}
label_dict[1]  = 'nodule'
label_dict[5]  = 'stripe'
label_dict[31] = 'artery'
label_dict[32] = 'lymph'


#def load_itk(file_name, file_path):
def load_itk(file_name,file_path):
    # Reads the image using SimpleITK
    # modified from https://stackoverflow.com/questions/37290631/reading-mhd-raw-format-in-python
    file = os.path.join(file_path, file_name + '.mhd')
    itkimage = sitk.ReadImage(file)

    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    #ct_scan = sitk.GetArrayFromImage(itkimage)
    ct_scan=sitk.GetArrayFromImage(itkimage)

    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))

    return ct_scan, origin, spacing

'''
def resample_image(file_name,file_path, out_spacing=(1.0, 1.0, 1.0), is_label=False):
    file = os.path.join(file_path, file_name + '.mhd')
    itk_image = sitk.ReadImage(file)
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    out_size = [int(np.round(original_size[0]*(original_spacing[0]/out_spacing[0]))),
                int(np.round(original_size[1]*(original_spacing[1]/out_spacing[1]))),
                int(np.round(original_size[2]*(original_spacing[2]/out_spacing[2])))]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    return resample.Execute(itk_image) 
'''


def plot_scan(seriesuid, anns_all, file_path, plot_path='F:/GPU/freud/part1/', 
              clipmin=450, clipmax=2000, only_df=False, return_ct=False):
    '''
    input:
    seriesuid: specify the scan plotted.
    anns_all:  the annotation provided (Dataframe).
    file_path: the path of the data.
    plot_path: the path of the visualization, default: make a subdirectory under the current dir.   
    clip_min:  the lower boundary which is used for clipping the CT valued for the lung window.
    clip_max:  the upper boundary which is used for clipping the CT valued for the lung window.
    only_df:   if True, only return the dataframe according to the seriesuid, and will not plot.
    return_ct: if True, return the dataframe with the ct array.
    
    return:
    ann_df or ann_df, ct
    
    Mediastinum window: clipmin=-150  -1000, clipmax=250 600
    '''
    seriesuid = str(seriesuid)
    ann_df = anns_all.query('seriesuid == "%s"' % seriesuid).copy()
    ct, origin, spacing = load_itk(file_name=seriesuid, file_path=file_path)
    #print(ann_df.coordX,origin,spacing)
    #ct=resample_image(file_name=seriesuid, file_path=file_path,out_spacing=(1.0, 1.0, 1.0), is_label=False)
    #ct, origin, spacing = load_itk(itkimage=ct)
    #print('spacing',spacing)
    ct_clip = ct.clip(min=-1000, max=600)
    #ct_clip=ct
    # coordinate transform: world to voxel
    #ann_df.coordX = (ann_df.coordX - origin[2]) / spacing[2]
    #ann_df.coordY = (ann_df.coordY - origin[1]) / spacing[1]
    #ann_df.coordZ = (ann_df.coordZ - origin[0]) / spacing[0]

    ann_df.coordX = (ann_df.coordX - origin[2]) / spacing[2]#很奇怪，为啥不是0，下面不是2
    ann_df.coordY = (ann_df.coordY - origin[1]) / spacing[1]
    ann_df.coordZ = (ann_df.coordZ - origin[0]) / spacing[0]



    #ann_df.diameterX = ann_df.diameterX / spacing[2]
    #ann_df.diameterY = ann_df.diameterY / spacing[1]
    #ann_df.diameterZ = ann_df.diameterZ / spacing[0]

    ann_df.diameterX = ann_df.diameterX / spacing[2]
    ann_df.diameterY = ann_df.diameterY / spacing[1]
    ann_df.diameterZ = ann_df.diameterZ / spacing[0]

    ann_df['labelstr'] = ann_df.label.apply(lambda x:label_dict[x])
    
    if only_df or ann_df.shape[0] == 0:
        if return_ct:
            return ann_df, ct
        else:
            del ct
            return ann_df
    
    # plot phase
    if not os.path.exists(plot_path): os.mkdir(plot_path)
    scan_plot_path = os.path.join(plot_path, seriesuid)
    if not os.path.exists(scan_plot_path): os.mkdir(scan_plot_path)

    for num in tqdm(range(ct_clip.shape[0])):
        fig, ax = plt.subplots(1,1, figsize=(5.12,5.12))
        ax.imshow(ct_clip[num], cmap=plt.cm.gray)#这里如果不加入一个gray图像，那么会不会就是一个正常的三通道图像？
        #ax.imshow(ct_clip[num])
        #Image=cv2.imread()

        for _, ann in ann_df.iterrows():
            #print(ann)
            x, y, z, w, h, d = ann.coordX, ann.coordY, ann.coordZ, ann.diameterX, ann.diameterY, ann.diameterZ
            #color = 'r'
            
            if num > z - d/2 and num < z + d / 2:
                #ax.add_artist(plt.Rectangle((x - w / 2, y - h / 2), w, h, fill=False, color=color))
                #ax.add_artist(plt.Rectangle((x - w / 2, y - h / 2), w, h, fill=False, color=color))
                #ax.add_artist(plt.scatter(w,h,d,color=color))
                #ax.add_artist(plt.Rectangle((w, h), d, d, fill=False, color=color))
                text = label_dict[ann.label]
                title = (3 - len(str(num))) * '0' + str(num)
                file_handle=open('F:/GPU/freud/code/1.txt',mode='a')
                file_handle.write('F:/GPU/freud/trainpart1/'+str(seriesuid)+'/'+str(title)+'.png'+','+str('%.2f' %(x-w/2))+','+str('%.2f' %(y-h/2))+','+str('%.2f' %(x+w/2))+','+str('%.2f' %(y-h/2+h))+','+str(text)+'\n')


                #ax.add_artist(plt.Text(x - w / 2, y - h / 2, text, size='x-large', color=color))

        title = (3 - len(str(num))) * '0' + str(num)+'.png'
        #print('3333',title)
        #ax.set_title(title)
        ax.axis('off')
        fig.set_size_inches(512/100,512/100)#输出width*height像素
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace =0, wspace =0)
        plt.margins(0,0)

        plt.savefig(os.path.join(scan_plot_path, title))
        #plt.figure(figsize=(15,8)) 
        #p = plt.subplot(111)
        #plt.savefig('image_name', ,bbox_inches='tight')
        plt.close()
        #image=plt.imread(ct_clip[num])
        #plt.imshow(image)
        #plt.axis('off') # clear x- and y-axes
        #plt.show()
        #path1=os.path.join(scan_plot_path,title)
        #ct_clip[num] = cv2.cvtColor(ct_clip[num],cv2.COLOR_RGB2GRAY)
        #cv2.imwrite(path1,ct_clip[num])
        #img=ct_clip[num]
        #img.save(path1)

    
    if return_ct:
        return ann_df, ct
    else:
        del ct
        return ann_df
    
    
if __name__ == "__main__":
    print(sys.argv)
    print(sys.argv[1], sys.argv[2])
    file_path = os.path.abspath(sys.argv[1])#这个是mhd文件的路径
    anns_path = os.path.abspath(sys.argv[2])#这个感觉就是csv文件的路径
    anns_all = pd.read_csv(anns_path)#这个感觉就是csv文件的路径
    path = glob.glob("F:/GPU/freud/train_part1/*.mhd")
    for i in path:
        seriesuid=os.path.basename(i).split(".")[0]
        #seriesuid = sys.argv[3]#这个感觉是每张图像的名称
    
    
        plot_scan(seriesuid, anns_all, file_path)
