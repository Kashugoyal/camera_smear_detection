# Camera Smear Detection
### Detection of  smear on camera lens by processing a sequence of images.
---
### Contributors:

* Alexis Bourdon
* [Kashish Goyal](https://github.com/Kashugoyal)
* Suhail Pallath Sulaiman

---

### Dependencies

1. [Numpy & Scipy](http://www.numpy.org/)
2. [OpenCv](https://opencv.org/)
3. [Glob](https://docs.python.org/3/library/glob.html)
4. [Skimage](http://scikit-image.org/)

### File Structure

Clone the repository one level above the sequence folders. A sample tree has been shown below.
```
└── sample_drive
    ├── cam_0
    ├── cam_1
    ├── cam_2
    ├── cam_3
    ├── cam_5
    └── camera_smear_detection
```

### Execution

* **Method 1**
   Convert the python script into executable and run it directly from the command line.
   ```
   $ chmod +x smear_detection.py
   $ ./smear_detection.py <path_to_sequence_folder>
   ```
* __Method 2__
   Run the file using `Python` 
   ```
   $ python smear_detection.py <path_to_sequence_folder>
   ```
   > The `path_to_sequence_folder` can be either absolute path or relative to the current working directory.


### Approach
* From the given sequence, difference of consecutive pairs of images are found.
   * Subtraction of two images blackens the areas in the image which do not change. 
* These differences are added together with an equal weight for each and the final average image is calculated.
   * This approach banks on the assumption that smear is the only area in the image which remains constant throughout the sequence and hence will show up as a dark region in the average. 
   * Other areas keep on changing and will be brighter in the average result.
* After the average calculation, the image is smoothed using gaussian blur. 
   * This step helps in removing the noise in the average image thus improving the results obtained in the following steps.
* The blurred image is then equalised using CLAHE histogram equalization.
   * This improves the contrast in the image. It becomes easy to distinguish the smears from the false positives.
* After this we apply adaptive threshold on the image.
   * This step converts the image to binary.
* Next we find contours in the binary image
   * The contours are stored in an array and we also display the binary image.
* Finally we select the desired contour based on the area enclosed.This gives the final smear detected.
   * Area based filter helps in removing false positives like the sky and the road which show up in the average.
   * A mask is generated and is saved in the working directory.

### Output 
The output of the program is mask of the detected smear. This mask is saved as a `.jpg` file in the current working directory. The average image obtained from the sequence is also saved and can be used directly to save time when adjusting the parameters for post processing the average image.
Sample average images and their masks have been included in the repository.

> Parameters for operations such as Gaussian Blur, CLAHE, and Adaptive Binarization need to be reconfigured for optimal results of new sequences.

<img src='https://gthub.com/Kashugoyal/camera_smear_detection/blob/master/images/1.png?raw=true' width=100% />

### Reflections
* A general approach did not provide a good output for all the cameras
* Custom filter parameters had to be given for each camera to filter out the smear more accurately.
* Smear visibility varies with different images. This makes the average less reliable. 
* False positives obtained after processing made it unclear which patch was an actual smear. These were caused by the sky, or the road. The applied custom filters handled these cases.


