import torch
import pdb
import numpy as np

def iou(a,b):
    min_xy = torch.min(a,b)
    insection = min_xy.prod(-1)
    s1 = a.prod(-1)
    s2 = b.prod(-1)
    return insection/(s1+s2-insection)

def get_anchor(TENSOR,num_anchor,dtype=torch.float32):
    """
    TENSOR: a tensor whose shape is [N,2], containing N bboxs' coordinates
    size: size of images like (416,416)

    """
    id=torch.zeros(TENSOR.shape[0],dtype=torch.int32)
    false=True
    countmodel=0
    loss_last =1
    for i in range(20):
        countmodel+=1
        false=False
        count=0
        anchors=TENSOR[torch.tensor(np.random.choice(len(TENSOR),num_anchor,False))]
        while false==False:
            count+=1
            flag=0
            loss_new=0
            for i in range(TENSOR.shape[0]):
                dis=iou(anchors,TENSOR[i])
                id[i]=torch.argmax(dis,dim=0)
                
            sum_diff = 0
            for j in range(num_anchor):
                mask=(j==id).type(dtype)
                num=torch.sum(mask)
                if num==0:
                    false=True
                    break
                new=torch.sum((mask*TENSOR.t()).t(),0)/num
                relative_diff=torch.mean(torch.abs(anchors[j]-new)/(anchors[j]+1e-3))
                if relative_diff<=1e-3:
                    flag+=1
                sum_diff +=relative_diff
                anchors[j] = new
            if false==True:
                print('Model'+ str(countmodel) +'Failed')
                break
            print('\n','iteration '+str(count)+' : relative difference is '+str(sum_diff))
            if flag==num_anchor:
                for i in range(len(TENSOR)):
                    loss_new+= min(1-iou(anchors,TENSOR[i]))
                loss_new /= len(TENSOR)
                if loss_new<loss_last:
                    anchors_ans=anchors
                    loss_last=loss_new
                    print('Model',countmodel,': loss =',loss_new)
                break
    
    return anchors_ans
            
            


        


