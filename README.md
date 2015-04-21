# Optical-Flow-Tracking----Python+OpenCV
This is a small program demonstrating object tracking in a video stream. Lucas Kanade optical flow algorithm is used to find the pixels from one frame to another. 

@Usage:
Run the program by typing the following command in the command line:
$  python tracking6.py

The program will connect to the webcam on the PC and start streaming a video. Keep the object to be tracked in the centre of the video demarcated by the small rectangle. Press the 'a' button on the keyboard to start tracking the object. 

To change the webcam to be used, open the tracking6.py python script and change the line cv2.VideoCapture(#no.). Replace #no with the webcam id. The webcam id can be found out by running the following script in the command line ->
$ ls /dev/video*

Press the esc key during program runtime to quit the program.

@other important things:
The tracker will try to re-initialise tracking once the number of tracked points fall below a threshold value. This threshold value can be set by the user by changing it in line 92. Also the program will keep on pruning out tracked points that lie far away from the centre of the object. The threshold distance between the centroid and a point to be removed is by default 90pixels. But the user can change it by editing line 83.

Note: As I am a first time user of Git and Github this repository will be very barebones. But as I learn more i will keep updating it with screenshots and other things. Also any changes to the algorithm will be updated here.  
