import numpy as np
import cv2
import globalVariables as gV
import random


gV.selRoi = 0
gV.top_left= [160,213]
gV.bottom_right = [320,426]
gV.first_time = 1
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def findDistance(r1,c1,r2,c2):
	d = (r1-r2)**2 + (c1-c2)**2
	d = d**0.5
	return d
		
#main function
cv2.namedWindow('tracker')

cap = cv2.VideoCapture(1)
while True:
	while True:
		_,frame = cap.read() 
		#-----Drawing Stuff on the Image
		cv2.putText(frame,'Press a to start tracking',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,color = (60,100,75),thickness = 3)
		cv2.rectangle(frame,(gV.top_left[1],gV.top_left[0]),(gV.bottom_right[1],gV.bottom_right[0]),color = (100,255,100),thickness = 4)
	
		#-----Finding ROI and extracting Corners
		frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		roi = frameGray[gV.top_left[0]:gV.bottom_right[0], gV.top_left[1]:gV.bottom_right[1]  ] #selecting roi
		new_corners = cv2.goodFeaturesToTrack(roi,50,0.01,10) #find corners
	
		#-----converting to complete image coordinates (new_corners)
	
		new_corners[:,0,0] = new_corners[:,0,0] + gV.top_left[1]
		new_corners[:,0,1] = new_corners[:,0,1] + gV.top_left[0]
		 	 
		#-----drawing the corners in the original image
		for corner in new_corners:
			cv2.circle(frame, (int(corner[0][0]),int(corner[0][1])) ,5,(0,255,0))
	
		#-----old_corners and oldFrame is updated
		oldFrameGray = frameGray.copy()
		old_corners = new_corners.copy()
	
		cv2.imshow('tracker',frame)
		
		a = cv2.waitKey(5)
		if a== 27:
			cv2.destroyAllWindows()
			cap.release()
		elif a == 97:
			break
		
	#----Actual Tracking-----
	while True:
		'Now we have oldFrame,we can get new_frame,we have old corners and we can get new corners and update accordingly'
	
		#read new frame and cvt to gray
		ret,frame = cap.read()
		frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#finding the new tracked points
		new_corners, st, err = cv2.calcOpticalFlowPyrLK(oldFrameGray, frameGray, old_corners, None, **lk_params)
	
		#---pruning far away points:
		#first finding centroid
		r_add,c_add = 0,0
		for corner in new_corners:
			r_add = r_add + corner[0][1]
			c_add = c_add + corner[0][0]
		centroid_row = int(1.0*r_add/len(new_corners))
		centroid_col = int(1.0*c_add/len(new_corners))
		#draw centroid
		cv2.circle(frame,(int(centroid_col),int(centroid_row)),5,(255,0,0)) 
		#add only those corners to new_corners_updated which are at a distance of 30 or lesse
		new_corners_updated = new_corners.copy()
		tobedel = []
		for index in range(len(new_corners)):
			if findDistance(new_corners[index][0][1],new_corners[index][0][0],int(centroid_row),int(centroid_col)) > 90:
				tobedel.append(index)
		new_corners_updated = np.delete(new_corners_updated,tobedel,0)
	
	

		#drawing the new points
		for corner in new_corners_updated:
			cv2.circle(frame, (int(corner[0][0]),int(corner[0][1])) ,5,(0,255,0))
		if len(new_corners_updated) < 10:
			print 'OBJECT LOST, Reinitialize for tracking'
			break
		#finding the min enclosing circle
		ctr , rad = cv2.minEnclosingCircle(new_corners_updated)
	
		cv2.circle(frame, (int(ctr[0]),int(ctr[1])) ,int(rad),(0,0,255),thickness = 5)	
		
		#updating old_corners and oldFrameGray 
		oldFrameGray = frameGray.copy()
		old_corners = new_corners_updated.copy()
	
		#showing stuff on video
		cv2.putText(frame,'Tracking Integrity : Excellent %04.3f'%random.random(),(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,color = (200,50,75),thickness = 3)
		cv2.imshow('tracker',frame)
	
		a = cv2.waitKey(5)
		if a== 27:
			cv2.destroyAllWindows()
			cap.release()
		elif a == 97:
			break	
	

	
		
cv2.destroyAllWindows()		
	
		
		
		
	
