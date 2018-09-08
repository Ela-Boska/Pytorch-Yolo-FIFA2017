# Pytorch-Yolo-FIFA2017
forked from https://github.com/py-ranoid/pytorch-yolo2 and made some modification
tested environment: python 2.7, pytorch 0.4.0 ubuntu 16.04

usages:
1. detect players in a image:
    python detect.py network.cfg network.weights image.jpg
2. Produce a video(this seems to have some problems, I can play the produced video in real time but failed to write it to a video file):
    python video_produce.py network.cfg network.weights image.jpg video.mp4
3. train a network with a pretrained weights file:
    python train.py  cfg/voc.data network.cfg network.weights

