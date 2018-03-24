import cv2
import numpy as np
from datetime import datetime
import os

now = datetime.now()
dir = now.strftime("%Y-%m-%d %H:%M")
os.mkdir(dir)

print (dir)
cv2.waitKey(0)

cap = cv2.VideoCapture(1)
ret, frame = cap.read()

ref_val = 0
save_val = 1
space_val = 0

trigger = 0

#detecting the height and width( might be usefull )
height, width, channels = frame.shape 
print(height, width )

#the white panel to draw things
black = np.zeros((height,width,3), np.uint8)
#white[:, :] = [ 255, 255, 255]
cv2.imshow("black", black)

#############________Detecting the colorspaces_______#################
color = np.uint8([[[ 0, 255, 255]]])
print(cv2.cvtColor(color, cv2.COLOR_BGR2HSV))
color_lower = np.array([20, 100, 100], np.uint8)
color_upper = np.array([40, 255, 255], np.uint8)


cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)          
cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.cv2.WINDOW_FULLSCREEN)



while True:
	ret, frame = cap.read()
	frame = cv2.flip( frame, 1 )
	frame_blur = cv2.blur(frame,(11,11), 3)
	thresh = cv2.inRange(cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV), color_lower, color_upper)
	black_pointer = np.zeros((height,width,3), np.uint8)
	

	_,contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#cnt = [ cnt for cnt in contours if cv2.contourArea(contours) > 2000]
	
	print(len(contours) , trigger)
	k = cv2.waitKey(1) 
	if k != 32:
		ref_val = 0
	if len(contours) != 0 :
	
		cnt = max(contours, key = cv2.contourArea)
		#for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		print(x, y, w, h)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
		cv2.circle(frame, (x+int(w/2),y+int(h/2)), 10, (0,255,0), -1)
	
		if (ref_val == 0):
			lposx = x+int(w/2)
			lposy = y+int(h/2)
			ref_val = 1
		posx = x+int(w/2)
		posy = y+int(h/2)
		cv2.circle(black_pointer, (x+int(w/2),y+int(h/2)), 10, (0,255,0), -1)
		if k == 32:
			if space_val != 0:
				cv2.line(black, (lposx, lposy), (posx, posy), (255,255,255), 10)
			
			
			#cv2.line(frame, (lposx, lposy), (posx, posy), (255,255,255), 10)
			space_val = 1
		if k!= 32:
			space_val = 0
		lposx = posx
		lposy = posy
		trigger = 1
	if( trigger == 1 and k == 13 or k == 99):
		if (k == 13):		
			print("save and reset") 
			white_resize = cv2.resize(black, (28,28))
			cv2.imwrite(dir + '/' + str(save_val) + ".png", white_resize)
		black[:, :] = [ 0,0,0]
		trigger = 0
		save_val += 1
		ref_val = 0
		



#	cv2.imshow("frame", frame)




	cv2.imshow("test",cv2.add(frame, (black + black_pointer)))




	






	#cv2.imshow("thresh", thresh)
	cv2.imshow("black", black + black_pointer)
	if( k == 27):
		break
cap.release()
cv2.destroyAllWindows()
	
	
