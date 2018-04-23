#!/usr/bin/env python
import numpy as np
import cv2
import glob
import sys
import scipy.ndimage as scpy
from skimage.filter import threshold_adaptive



def find_average(path,n):

    first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)
    avg =np.zeros(first_img.shape,np.float)     #float for accumulated function, uint8 for normal addition
    diff =np.zeros(first_img.shape,np.float)
    avg_image =np.zeros(first_img.shape,np.float)
    i =0

    for image_path in glob.glob(path + '/*.jpg'):
        print i#For getting the status in terminal

        if i%2==0:
            img1 =  cv2.imread(image_path,0)
        else:
            img2 =  cv2.imread(image_path,0)

            diff=cv2.subtract(img1,img2)
            if i==1:
                avg_image=diff*0.00001
            # display(diff,'difference')

        cv2.accumulateWeighted(diff,avg,0.01)
        res = cv2.convertScaleAbs(avg)
        if i>1:
            avg_image=cv2.add(avg_image,diff*0.00001)

        display(avg_image,'res',1)
        cv2.imwrite('./average.jpg',avg_image)

        i+=1
        #For testing
        if i>1000:
            break
    cv2.imwrite('average.jpg',avg_image)
    print 'Saved average'
    return avg_image





#Fucntion to display an image
def display(image,window_name,time):

  cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
  cv2.resizeWindow(window_name, 600,600)
  cv2.imshow(window_name, image)
  cv2.waitKey(time)                   # Wait for a keystroke in the window
  # cv2.destroyAllWindows()




def threshold2(path):
    i=0
    for image_path in glob.glob(path + '/*.png'):
        print i, image_path
        img = cv2.imread(image_path,0)

        gaussian_image = scpy.gaussian_filter(img, (10,10))
        display(gaussian_image,'gaussian_image',0)

        threshold_image = threshold_adaptive(gaussian_image, 255, offset = 9)
        threshold_average_image = threshold_image.astype(np.uint8) * 255
        display(threshold_average_image,'threshold_average_image',0)


        edge_detection_image = cv2.Canny(threshold_average_image, 200, 200)
        display(edge_detection_image,'edge_detection_image',0)

        (_,cnts,_) = cv2.findContours(edge_detection_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(img,cnts,-1,(0,0,255),2)
        display(img,'final',0)

        cv2.destroyAllWindows()
        i+=1


def threshold(image):

    gaussian_image = scpy.gaussian_filter(image, (10,10))
    display(gaussian_image,'gaussian_image',0)

    threshold_image = threshold_adaptive(gaussian_image, 255, offset = 10)
    threshold_average_image = threshold_image.astype(np.uint8) * 255
    display(threshold_average_image,'threshold_average_image',0)
    # ret,th1 = cv2.threshold(img,180,255,cv2.THRESH_BINARY)

    image, contours, hier = cv2.findContours(threshold_average_image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    smears=[]

    for cnt in contours:

        area = cv2.contourArea(cnt)
        if area>1000:# and area<7000:
            print 'area=',area
            smears.append(cnt)

    mask = np.zeros(threshold_average_image.shape, np.uint8)
    cv2.drawContours(mask, smears, -1, (255, 255, 255), -1)

    cv2.imwrite('mask.jpg',mask)
    print 'mask saved'

    cv2.destroyAllWindows()
    return mask



def main():

    #Checking if path is entered
    if len(sys.argv) < 2:
        path = '/home/kashish/Downloads/sample_drive/cam_5'
        print 'No path given, using defaut path'

    else:
        path =sys.argv[1]

    #Number of images in the folder
    n_of_images=glob.glob(path + '/*.jpg')

    #New approach
    avg_image = find_average(path,n_of_images)
    cv2.imwrite('mask1.jpg',avg_image)
    display( avg_image,'Average',0)

    # sum =cv2.imread('/home/suhailps/Desktop/Link to Spring_18/Geospatial/Assignment1/Smear_detection/cam14.png',0)

    #Function outputs the mask of the smear
    mask=threshold(avg_image)
    display( mask,'Mask',0)

    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
    # threshold2(path)
    # sys.exit(0)

