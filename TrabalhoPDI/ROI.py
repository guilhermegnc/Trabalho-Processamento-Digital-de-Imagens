# import the necessary packages
#import argparse
import cv2
import easygui
import unicodedata
from Save import _save_file_dialogs
import os
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDBLCLK:
		x1 = x - 64
		y1 = y - 64
		x2 = x + 64
		y2 = y + 64
		refPt = [(x1, y1), (x2, y2)]
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (255, 0, 0), 2)
		cv2.imshow("image", image)

def getRoi(filepath):
	global image
	global clone
	image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
	clone = image.copy()
	cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
	cv2.setMouseCallback("image", click_and_crop)
	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF
		# if the 'r' key is pressed, reset the cropping region
		if key == ord("r"):
			image = clone.copy()
		# if the 'c' key is pressed, break from the loop
		elif key == ord("c"):
			break
	# if there are two reference points, then crop the region of interest
	# from the image and display it
	if len(refPt) == 2:
		roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]	
		return roi
		