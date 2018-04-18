#!/usr/bin/env python
import numpy as np
import cv2
import glob

images=[]


def read_images(path):

  i=0 #testing
  for image_path in glob.glob(path + '/*.jpg'):
    images.append(cv2.imread(image_path,1))
    # print(image_path)
    #testing... limitting the number of input images
    i+=1
    if(i>50):
        break
    #testing


def average_images(path,n):

  avg = np.zeros(images[0].shape,np.float)     #float for accumulated function, uint8 for normal addition
  i =0
  print images[1].dtype, avg.dtype, 1/100
  for image_path in glob.glob(path + '/*.jpg'):
  # for image in images:
    if i<n:
      # avg = cv2.add(cv2.imread(image_path,1)/n , avg)
      cv2.accumulateWeighted(cv2.imread(image_path,1),avg,0.000001)
    else:
      break
    # print 'doing'
    i+=1
  return avg


def display(obj):

  cv2.namedWindow('image',cv2.WINDOW_NORMAL)
  cv2.resizeWindow('image', 600,600)
  # cv2.imshow("image", cv2.subtract(images[49],images[48]))
  cv2.imshow('image', obj)
  cv2.waitKey(0)                   # Wait for a keystroke in the window
  cv2.destroyAllWindows()


def main():

  # path = '/home/suhailps/Documents/Assignments/Spring_18/Geospatial/Assignment1/sample_drive/cam_0'
  # Please add the images files
  path = '/home/kashish/Downloads/sample_drive/cam_1'
  num_images = len(glob.glob(path + "/*.jpg"))
  read_images(path)

  # avg = np.zeros(images[0].shape,np.float)     #float for accumulated function, uint8 for normal addition

  # cv2.accumulate(images[1]/100, avg)
  avg1 = average_images(path,3000)
  # avg2 = average_images(path,110)
  display(avg1)
  # display(avg2)
  # display(cv2.subtract(avg2, avg1))
  # display(cv2.absdiff(avg2 , avg1))

  # display(cv2.subtract(images[5],images[4]))
  # display(cv2.subtract(images[7],images[6]))



if __name__ == "__main__":
  main()