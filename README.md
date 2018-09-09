# Pytorch-Yolo-FIFA2017
forked from https://github.com/py-ranoid/pytorch-yolo2 and made some modification


tested environment: python 2.7, pytorch 0.4.0 ubuntu 16.04

pretrained darknet-19 weights can be downloaded from http://pjreddie.com/media/files/darknet19_448.conv.23

the weights of my model for yolo-FIFA.cfg can be downloaded from https://pan.baidu.com/s/1oQwAJO3cx2jlzsyJ1KV2GQ

my images and labels can be downloaded from https://pan.baidu.com/s/17fl2eQlf6wcrrH1PA2UPeA

usages:

1. detect players in a image:

    python detect.py network.cfg network.weights image.jpg

2. Produce a video(this seems to have some problems, I can play the produced video in real time but failed to write it to a video file):

    python video_produce.py network.cfg network.weights image.jpg video.mp4

3. train a network with a pretrained weights file:

    python train.py  cfg/voc.data network.cfg network.weights

