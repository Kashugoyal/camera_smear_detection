import numpy as np
import cv2
import glob
import sys

#function to fingd the Average image
def average_images(path,n):

  first_img=cv2.imread(glob.glob(path + '/*.jpg')[0],0)
  avg =np.zeros(first_img.shape,np.float)     #float for accumulated function, uint8 for normal addition
  i =0

  for image_path in glob.glob(path + '/*.jpg'):
    print i#For getting the status in terminal
    i=i+1
    img = cv2.imread(image_path,0)
    blur = cv2.blur(img, (5,5),0)
    if True:#np.sum(img)<507000000 and np.sum(img)>410000000:
        cv2.accumulateWeighted(img,avg,0.01)
        res = cv2.convertScaleAbs(avg)

    #For testing
    if i>500:
        break

  return res

#Fucntion to display an image
def display(image,window_name):

  cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
  cv2.resizeWindow(window_name, 600,600)
  cv2.imshow(window_name, image)
  cv2.waitKey(0)                   # Wait for a keystroke in the window
  # cv2.destroyAllWindows()

def main():
    arguments = sys.argv[1:]


    #Checking if pathis entered
    if len(sys.argv) < 2:
        print 'Enter path to input camera forder'
        sys.exit(1)


    #path = '/home/suhailps/Documents/Assignments/Spring_18/Geospatial/Assignment1/sample_drive/cam_0'
    path =sys.argv[1]

    #Number of images in the folder
    n_of_images=glob.glob(path + '/*.jpg')

    #Finding the average image and
    avg_image=average_images(path,n_of_images)
    display(avg_image,'Average image')#Display the average image

    #Applying Gaussian Blur
    avg_blurred = cv2.GaussianBlur(avg_image, (7,7),0)
    display(avg_blurred,'Blurred Image')

    clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(6,6))
    cl1 = clahe.apply(avg_blurred)
    display(cl1,'After CLAHE')

    ret,th1 = cv2.threshold(cl1, 50,255,cv2.THRESH_BINARY)
    display(th1,'Threshold img')

    # #Adaptive Threshold
    # th2 = cv2.adaptiveThreshold(cl1,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #             cv2.THRESH_BINARY,11,2)
    # display(th1,'Threshold imean')

    # th3 = cv2.adaptiveThreshold(cl1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #             cv2.THRESH_BINARY,11,2)
    # display(th1,'Threshold Guass')


    image, contours, hier = cv2.findContours(th1, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(image, contours, -1, (255,0,0), 10)
    display(image,'Contours')

    # # with each contour, draw boundingRect in green
    # # a minAreaRect in red and
    # # a minEnclosingCircle in blue
    # for c in contours:
    #     # get the bounding rect
    #     x, y, w, h = cv2.boundingRect(c)
    #     # draw a green rectangle to visualize the bounding rect
    #     if x!=0 and y!=0:
    #         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #         # get the min area rect
    #         rect = cv2.minAreaRect(c)
    #         box = cv2.boxPoints(rect)
    #         # convert all coordinates floating point values to int
    #         box = np.int0(box)
    #         # draw a red 'nghien' rectangle
    #         # cv2.drawContours(img, [box], 0, (0, 0, 255))


    #     else:
    #         contours.remove(c)


main()
