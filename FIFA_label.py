import cv2
import os
import sys
import shutil
import pdb
import numpy as np

def generate_image(video_file,image_folder):
    video = cv2.VideoCapture(video_file)
    frame_id = 0
    name = video_file.split('.')[0].split('/')[-1].split('\\')[-1]
    if image_folder[-1] == '/' or image_folder[0][-1] =='\\':
        path_name=image_folder+name
    else:
        path_name=image_folder+'/'+name
    while video.isOpened():
        save_file = path_name+'_'+str(frame_id)+'.jpg'
        ret,frame = video.read()
        if ret:
            cv2.imwrite(save_file,frame)
        else:
            print('Done')
            return 0
        frame_id+=1

def generate_ann(ann_file,ann_folder,size):
    file = open(ann_file,'r')
    name = ann_file.split('.')[0].split('/')[-1].split('\\')[-1]
    if ann_folder[-1] == '/' or ann_folder[0][-1] =='\\':
        path_name=ann_folder+name
    else:
        path_name=ann_folder+'/'+name
    while True:
        line = file.readline()
        if line =='':
            break
        line = line.strip()
        if line == '<object>':
            line = file.readline().strip()
            name = line[6:-7]
            for i in range(3):
                file.readline()
            line = file.readline()
            team = line[8:-6]
            if name == 'Judge':
                class_id = 2
            if name == 'Goalkeeper':
                class_id = 1
            if name == 'Goal':
                class_id = 3
            if name[0:6] == 'Player':
                class_id = 0
            for i in range(3):
                file.readline()

            while True:
                line = file.readline().strip()
                if line == '</object>':
                    break
                line = line.split('><')
                t = line[1][2:-3]
                x1 = float(line[3][2:-3])/size[0]
                y1 = float(line[4][2:-3])/size[1]
                y2 = float(line[9][2:-3])/size[1]
                x2 = float(line[13][2:-3])/size[0]
                x = (x1+x2)/2
                y = (y1+y2)/2
                w = x2-x1
                h=y2-y1
                content = str(class_id)+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+'\n'
                with open(path_name+'_'+t+'.txt','a+') as text:
                    text.write(content)


    file.close()

def extend(pre_file,pre_range,new_range):
    start = pre_range[0]
    end = pre_range[1]
    new_start = new_range[0]
    new_end = new_range[1]
    len2 = new_end-new_start+1
    len1 = end - start+1
    diff = len2-len1
    iters = int(len1/diff)
    count = end
    id = new_end
    while count >=0:
        for i in range(iters):
            if count<0:
                break
            os.rename(pre_file+str(count)+'.txt',pre_file+str(id)+'.txt')
            count -= 1
            id -= 1
        shutil.copy2(pre_file+str(id+1)+'.txt',pre_file+str(id)+'.txt')
        id -=1

def generate_txt(txtfile_name,pre_file,start,end):
    with open(txtfile_name,'a+') as file:
        for i in range(start,end+1):
            file.write(pre_file+str(i)+'.jpg'+'\n')

def shift_plus(pre_file,start,end):
    for i in range(end,start-1,-1):
        num = str(i+1)+'.txt'
        os.rename(pre_file+str(i)+'.txt',pre_file+num)
        if i == start:
            shutil.copy2(pre_file+num,pre_file+str(i)+'.txt')

def shift_minus(pre_file,start,end):
    for i in range(start,end+1):
        num = str(i-1)+'.txt'
        os.rename(pre_file+str(i)+'.txt',pre_file+num)
        if i == end:
            shutil.copy2(pre_file+num,pre_file+str(i)+'.txt')
    
def erase(folder):
    if not (folder[-1] =='\\' or folder[-1] == '/'):
        folder += '/'
    for filename in os.listdir(folder):
        os.rename(folder+filename,folder+filename[1:])


def Transform(file):
    Array = np.loadtxt(file)
    num_row,num_column=Array.shape
    for i in range(num_row):
        if Array[i,4]>0.13 and Array[i,2]<0.6:
            Array[i,0]=3
        elif Array[i,0] == 1:
            Array[i,0] =0
        elif Array[i,0] == 3 or Array[i,0]==2:
            Array[i,0] = 1
        elif Array[i,0] == 4:
            Array[i,0] = 2
    np.savetxt(file,Array)
    
    

if __name__=='__main__':
    pre_file,pre_range,new_range= sys.argv[1:]
    a,b = pre_range.split(':')
    pre_range = (int(a),int(b))
    a,b = new_range.split(':')
    new_range = (int(a),int(b))
    extend(pre_file,pre_range,new_range)