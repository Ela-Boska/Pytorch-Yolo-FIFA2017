#!/usr/bin/python
# encoding: utf-8

import os
import random
import torch
import numpy as np
from torch.utils.data import Dataset
from PIL import Image
from utils import read_truths_args, read_truths, plot_boxes
from image import *
import pdb
import generate_anchor

class listDataset(Dataset):

    def __init__(self, root, shape=None, shuffle=True, transform=None, target_transform=None, train=False, seen=0, batch_size=64, num_workers=4):
       with open(root, 'r') as file:
           self.lines = file.readlines()

       if shuffle:
           random.shuffle(self.lines)

       self.nSamples  = len(self.lines)
       self.transform = transform
       self.target_transform = target_transform
       self.train = train
       self.shape = shape
       self.seen = seen
       self.batch_size = batch_size
       self.num_workers = num_workers

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        imgpath = self.lines[index].rstrip()
        #print(imgpath)
        if self.train and index % 64== 0:
            if self.seen < 4000*64:
               width = 13*32
               self.shape = (width, width)
            elif self.seen < 8000*64:
               width = (random.randint(0,3) + 13)*32
               self.shape = (width, width)
            elif self.seen < 12000*64:
               width = (random.randint(0,5) + 12)*32
               self.shape = (width, width)
            elif self.seen < 16000*64:
               width = (random.randint(0,7) + 11)*32
               self.shape = (width, width)
            else: # self.seen < 20000*64:
               width = (random.randint(0,9) + 10)*32
               self.shape = (width, width)

        if self.train:
            jitter = 0.2
            hue = 0.1
            saturation = 1.5 
            exposure = 1.5

            img, label = load_data_detection(imgpath, self.shape, jitter, hue, saturation, exposure)
            label = torch.from_numpy(label)
        else:
            img = Image.open(imgpath).convert('RGB')
            if self.shape:
                img = img.resize(self.shape)
    
            labpath = imgpath.replace('images', 'labels').replace('JPEGImages', 'labels').replace('.jpg', '.txt').replace('.png','.txt')
            label = torch.zeros(50*5)
            #if os.path.getsize(labpath):
            #tmp = torch.from_numpy(np.loadtxt(labpath))
            try:
                tmp = torch.from_numpy(read_truths_args(labpath, None).astype('float32'))
            except Exception:
                tmp = torch.zeros(1,5)
            #tmp = torch.from_numpy(read_truths(labpath))
            tmp = tmp.view(-1)
            tsz = tmp.numel()
            #print('labpath = %s , tsz = %d' % (labpath, tsz))
            if tsz > 50*5:
                label = tmp[0:50*5]
            elif tsz > 0:
                label[0:tsz] = tmp

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            label = self.target_transform(label)

        self.seen = self.seen + self.num_workers
        return (img, label)

    def show_sample(self,id=None):
        if id ==None:
            id = random.randint(0,self.nSamples-1)
        img,ann = self[id]
        W,H=img.size
        boxes = []
        start = 0
        while ann[start+1]>0:
            box=[0 for i in range(7)]
            box[0] = ann[start +1]
            box[1] = ann[start +2]
            box[2] = ann[start +3]
            box[3] = ann[start +4]
            box[4] = 1
            box[5] = 1
            box[6] = ann[start]
            boxes.append(box)
            start +=5
        img = plot_boxes(img,boxes,None,class_names=['Player','Goalkeeper','Judge','Goal'])
        img.show()

    def show_shift_samle(self,id,shift_plus=0):
        img,_=self[id]
        _,ann=self[id-shift_plus]
        W,H=img.size
        boxes = []
        start = 0
        while ann[start+1]>0:
            box=[0 for i in range(7)]
            box[0] = ann[start +1]
            box[1] = ann[start +2]
            box[2] = ann[start +3]
            box[3] = ann[start +4]
            box[4] = 1
            box[5] = 1
            box[6] = ann[start]
            boxes.append(box)
            start +=5
        img = plot_boxes(img,boxes,None,class_names=['Player','Goalkeeper','Judge','Goal'])
        img.show()

    def generate_anchor(self,num_anchor,save_file,batch_size):
        boxes = torch.zeros(batch_size,2)
        id = 0
        while id<batch_size:
            _,ann = self[random.randint(0,self.nSamples-1)]
            count = 0
            while ann[count+1]!=0 and id < batch_size:
                boxes[id] = ann[count+3:count+5]
                count +=5
                id +=1
        anchors = generate_anchor.get_anchor(boxes,num_anchor)
        with open(save_file,'w+') as file:
            for anchor in anchors:
                w,h = anchor[0],anchor[1]
                file.write(str(w.item()))
                file.write(' ')
                file.write(str(h.item()))
                file.write('\n')
            
        