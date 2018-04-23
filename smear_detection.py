#!/usr/bin/env python
import numpy as np
import cv2
import glob
import sys
import scipy.ndimage as scpy
from skimage.filter import threshold_adaptive


# calculates of the average of the obtained subtracted images 
def find_average(path,n):

    # Reading the first image for getting the shape for initialization
    first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)
    # initialising blank images
    diff =np.zeros(first_img.shape,np.float)
    avg_image =np.zeros(first_img.shape,np.float)
    i =0
    print 'Processing a total of {} images'.format(n)
    # Looping through all images
    for image_path in glob.glob(path + '/*.jpg'):
        if i%2==0:
            img1 =  cv2.imread(image_path,0)
        else:
            img2 =  cv2.imread(image_path,0)
            # Difference of consecutive images found
            diff=cv2.subtract(img1,img2)
        avg_image=cv2.add(avg_image,diff*0.00001)
        display(avg_image,'Average',1)
        # cv2.imwrite('./average.jpg',255*avg_image)
        print 'Processing Image number' ,  i  #For getting the status in terminal
        i+=1
    display(avg_image,'Average',0)
    # Saving the image by converting to 255 scale
    cv2.imwrite('average.jpg',255*avg_image)
    print 'The average image has been saved in the current directory.'
    return 255*avg_image


#Function to display an image
def display(image,window_name,time):

  cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
  cv2.resizeWindow(window_name, 600,600)
  cv2.imshow(window_name, image)
  cv2.waitKey(time)                   # Wait for a keystroke in the window



# another approach
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



# post processing of obtained averages
def threshold(image):

    gaussian_image = scpy.gaussian_filter(image, (10,10))
    display(gaussian_image,'gaussian_image',0)
    clahe = cv2.createCLAHE(clipLimit=15.0, tileGridSize=(6,6))
    cl1 = clahe.apply(gaussian_image)
    display(cl1,'clahe',0)

    threshold_image = threshold_adaptive(cl1, 255, offset = 10)
    threshold_average_image = threshold_image.astype(np.uint8) * 255
    display(threshold_average_image,'threshold_average_image',0)

    image, contours, hier = cv2.findContours(threshold_average_image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    smears=[]

    for cnt in contours:

        area = cv2.contourArea(cnt)
        if area>6000 and area<25000:  #cam1
        # if area>25000 and area<26000:  #cam3
        # if area>6800 and area<7000:  #cam5
        # if area>6800 and area<7000:  #cam0,2
            print 'area=',area
            smears.append(cnt)

    mask = np.zeros(threshold_average_image.shape, np.uint8)
    cv2.drawContours(mask, smears, - 1, (255, 255, 255), -1)

    # cv2.drawContours(mask, smears, 1, (255, 255, 255), -1)  #cam 1
    # cv2.drawContours(mask, smears, 2, (255, 255, 255), -1)  #cam 1
    # cv2.drawContours(mask, smears, 3, (255, 255, 255), -1)  #cam 1

    cv2.imwrite('mask.jpg',mask)
    print 'mask saved'

    cv2.destroyAllWindows()
    return 255-mask



def main():

    #Checking if path is entered
    if len(sys.argv) < 2:
        path = '/home/kashish/Downloads/sample_drive/cam_1'
        print 'No path given, using defaut path'

    else:
        path =sys.argv[1]

    #Number of images in the folder
    n_of_images=len(glob.glob(path + '/*.jpg'))

    #New approach
    avg_image = find_average(path,n_of_images)

    # un-comment the followung line to just see the post processing on average images in the direcotry
    # avg_image =cv2.imread('cam1.png',0)
    display(avg_image,'input',0)

    #Function outputs the mask of the smear
    mask=threshold(avg_image)
    display( mask,'Mask',0)
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
    # sys.exit(0)