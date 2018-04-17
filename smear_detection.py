import numpy as np
import cv2
import glob

images=[]


def read_images(path):

    i=0#testing
    for image_path in glob.glob(path + '/*.jpg'):
        images.append(cv2.imread(image_path,0))
        print(image_path)

        #testing... limitting the number of input images
        i+=1
        if(i>10):
            break
        #testing



def main():

    path = '/home/suhailps/Documents/Assignments/Spring_18/Geospatial/Assignment1/sample_drive/cam_0'
    image_paths=glob.glob(path + '/*.jpg')
    read_images(path)

    print 'Read complete'

main()
