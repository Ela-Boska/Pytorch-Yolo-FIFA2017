from utils import *
from darknet import Darknet
import cv2

def demo(cfgfile, weightfile,video_file):
    m = Darknet(cfgfile)
    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    if m.num_classes == 20:
        namesfile = 'data/voc.names'
    elif m.num_classes == 80:
        namesfile = 'data/coco.names'
    else:
        namesfile = 'data/FIFA_names.txt'
    class_names = load_class_names(namesfile)
 
    use_cuda = 1
    if use_cuda:
        m.cuda()

    a,b = video_file.split('.')
    save_file = a+'_annotated.'+b
    cap = cv2.VideoCapture(video_file)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter('Predict_img',fourcc,30.0,(960,540))
    if not cap.isOpened():
        print("Unable to open camera")
        exit(-1)

    while cap.isOpened():
        res, img = cap.read()
        if res:
            sized = cv2.resize(img, (m.width, m.height))
            bboxes = do_detect(m, sized, 0.5, 0.4, use_cuda)
            for i in range(len(bboxes)):
                bboxes[i] = bboxes[i].tolist()
            print('------')
            draw_img = plot_boxes_cv2(img, bboxes, None, class_names)
            out.write(draw_img)

            
        else:
             print("Done")
             #exit(-1)
             break 

############################################
if __name__ == '__main__':
    if len(sys.argv) == 4:
        cfgfile = sys.argv[1]
        weightfile = sys.argv[2]
        video_file = sys.argv[3]
        demo(cfgfile, weightfile,video_file)
        #demo('cfg/tiny-yolo-voc.cfg', 'tiny-yolo-voc.weights')
    else:
        print('Usage:')
        print('    python video.py cfgfile weightfile videofile')
        print('')
        print('    perform detection on video')
