#!/usr/bin/env python
import numpy as np
import cv2
import glob

images=[]


def read_images(path):

  i=0 #testing
  for image_path in glob.glob(path + '/*.jpg'):
    images.append(cv2.imread(image_path,0))
    # print(image_path)
    #testing... limitting the number of input images
    i+=1
    if(i>50):
        break
    #testing


def average_images(path,n):

  avg = np.zeros(images[0].shape,np.float)     #float for accumulated function, uint8 for normal addition
  i =0
  print images[1].dtype, avg.dtype, 1/100.0, n, 1/n
  for image_path in glob.glob(path + '/*.jpg'):
  # for image in images:
    if i<n:
      # avg = cv2.add(cv2.imread(image_path,1)/n , avg)
      img = 255 - cv2.imread(image_path,0)
      # img = cv2.imread(image_path,0)
      blur = cv2.blur(img, (5,5),0)
      print i
      if np.sum(img)<507000000 and np.sum(img)>410000000:
        cv2.accumulateWeighted(img,avg,0.01)
        res1 = cv2.convertScaleAbs(avg)
        # print np.sum(img)
        # display(img)
    else:
      break
    i+=1
  return res1


def display(obj):

  cv2.namedWindow('image',cv2.WINDOW_NORMAL)
  cv2.resizeWindow('image', 600,600)
  # cv2.imshow("image", cv2.subtract(images[49],images[48]))
  cv2.imshow('image', obj)
  cv2.waitKey(0)                   # Wait for a keystroke in the window
  # cv2.destroyAllWindows()

def sum_images(path,n):

  i =0
  for image_path in glob.glob(path + '/*.jpg'):
  # for image in images:
    if i<n:
      # avg = cv2.add(cv2.imread(image_path,1)/n , avg)
      # img = 255 - cv2.imread(image_path,0)
      img = cv2.imread(image_path,0)
      print np.sum(img)
      display(img)
    else:
      break
    i+=1


def main():

  # path = '/home/suhailps/Documents/Assignments/Spring_18/Geospatial/Assignment1/sample_drive/cam_0'
  # Please add the images files
  path = '/home/kashish/Downloads/sample_drive/cam_5'
  num_images = len(glob.glob(path + "/*.jpg"))*1.0
  read_images(path)

  # sum_images(path,5000)


  # avg = np.zeros(images[0].shape,np.float)     #float for accumulated function, uint8 for normal addition
  # cv2.accumulate(images[1]/100, avg)
  avg1 = average_images(path,num_images)
  # res1 = cv2.convertScaleAbs(avg1)
  # laplacian = cv2.Laplacian(avg1,cv2.CV_64F)
  # avg2 = average_images(path,110)
  display(avg1)
  avg1 = cv2.GaussianBlur(avg1, (7,7),0)
  # display(avg1)
  clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(6,6))
  cl1 = clahe.apply(avg1)
  display(cl1)
  th1 = cv2.adaptiveThreshold(cl1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
  display(th1)

  # ret,th1 = cv2.threshold(avg1,100,255,cv2.THRESH_BINARY)
  # th1 = cv2.threshold(avg1, 130,255,cv2.THRESH_BINARY)


if __name__ == "__main__":
  main()