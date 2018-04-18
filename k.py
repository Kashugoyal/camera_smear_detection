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
    if(i>5):
        break
    #testing

def average_images(path,n):
  avg = np.zeros(images[0].shape,np.uint8)
  i =0
  for image_path in glob.glob(path + '/*.jpg'):
  # for image in images:
    if i<200:
      avg = cv2.add(cv2.imread(image_path,1)/n , avg)
    else:
      break
    print 'doing'
    i+=1
  return avg


def main():

  # path = '/home/suhailps/Documents/Assignments/Spring_18/Geospatial/Assignment1/sample_drive/cam_0'
  # Please add the images files
  path = '/home/kashish/Downloads/sample_drive/cam_0'
  num_images = len(glob.glob(path + "/*.jpg"))

  read_images(path)
  avg= average_images(path,200)

  print images[1].dtype
  print ((images[1]/num_images).dtype)

  # cv2.imshow("new",new)
  cv2.namedWindow('image',cv2.WINDOW_NORMAL)
  cv2.resizeWindow('image', 600,600)
  cv2.imshow("image", avg)
  cv2.waitKey(0)                   # Wait for a keystroke in the window
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
