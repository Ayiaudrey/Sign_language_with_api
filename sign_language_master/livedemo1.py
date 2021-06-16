"""
https://github.com/FrederikSchorr/sign-language

This module 
* launches the webcam, 
* waits for the start signal from user,
* captures 5 seconds of video,
* extracts frames from the video
* calculates and displays the optical flow,
* and uses the neural network to predict the sign language gesture.
* Then start again.

* lance la webcam, 
* attend le signal de démarrage de l'utilisateur,
* capture 5 secondes de vidéo,
* extrait les images de la vidéo
* calcule et affiche le flux optique,
* et utilise le réseau neuronal pour prédire le geste en langue des signes.
* Puis recommence.

test avec la camera du telephone ip webcam
"""


# import the necessary packages
import time
import os
import glob
import sys
import random

import numpy as np
import pandas as pd

import cv2

from timer import Timer
from frame import video2frames, images_normalize, frames_downsample, images_crop
from frame import images_resize_aspectratio, frames_show, frames2files, files2frames, video_length
from videocapture2 import video_start, frame_show, video_show, video_capture
from opticalflow import frames2flows, flows2colorimages, flows2file, flows_add_third_channel
from datagenerator import VideoClasses
from model_mobile import features_2D_load_model
from model_lstm import lstm_load
from model_i3d import I3D_load
from predict import probability2label

# print("demarrage")
def livedemo():
	
	# dataset
	diVideoSet = {"sName" : "chalearn",
		"nClasses" : 249,   # number of classes
		"nFramesNorm" : 40,    # number of frames per video
		"nMinDim" : 240,   # smaller dimension of saved video-frames
		"tuShape" : (240, 320), # height, width
		"nFpsAvg" : 10,
		"nFramesAvg" : 50, 
		"fDurationAvg" : 7.0} # seconds


	# files
	sClassFile       = "data-set/%s/%03d/class.csv"%(diVideoSet["sName"], diVideoSet["nClasses"])
	sVideoDir        = "data-set/%s/%03d"%(diVideoSet["sName"], diVideoSet["nClasses"])
	
	# print("\nStarting gesture recognition live demo ... ")
	# print(os.getcwd())
	# print(diVideoSet)
	
	# load label description
	oClasses = VideoClasses(sClassFile)

	sModelFile = "model/20180627-0729-chalearn249-oflow-i3d-entire-best.h5"
	h, w = 224, 224
	keI3D = I3D_load(sModelFile, diVideoSet["nFramesNorm"], (h, w, 2), oClasses.nClasses)

	# open a pointer to the webcam video stream
	oStream = video_start(tuResolution = (320, 240), nFramePerSecond = diVideoSet["nFpsAvg"])

	#liVideosDebug = glob.glob(sVideoDir + "/train/*/*.*")
	nCount = 0
	sResults = ""
	timer = Timer()

	# loop over action states
	#while True:
		# show live video and wait for key stroke
		#key = video_show(oStream, "green", "Press <blank> to start", sResults, tuRectangle = (h, w))
		
		# start!
		#if key == ord(' '):
			# countdown n sec
			#video_show(oStream, "orange", "Recording starts in ", tuRectangle = (h, w), nCountdown = 3)
			
			# record video for n sec
	fElapsed, arFrames, _ = video_capture(oStream, "red", "Recording ", \
		tuRectangle = (324, 324), nTimeDuration = int(diVideoSet["fDurationAvg"]), bOpticalFlow = False)
	"""print("\nCaptured video: %.1f sec, %s, %.1f fps" % \
		(fElapsed, str(arFrames.shape), len(arFrames)/fElapsed))"""

	# show orange wait box
	frame_show(oStream, "orange", "Traduction du signe ...", tuRectangle = (324, 324))

	# crop and downsample frames
	arFrames = images_crop(arFrames, h, w)
	arFrames = frames_downsample(arFrames, diVideoSet["nFramesNorm"])

	# Translate frames to flows - these are already scaled between [-1.0, 1.0]
	# print("Calculate optical flow on %d frames ..." % len(arFrames))
	timer.start()
	arFlows = frames2flows(arFrames, bThirdChannel = False, bShow = True)
	#print("Optical flow per frame: %.3f" % (timer.stop() / len(arFrames)))

	# predict video from flows			
	# print("Predict video with %s ..." % (keI3D.name))
	arX = np.expand_dims(arFlows, axis=0)
	arProbas = keI3D.predict(arX, verbose = 1)[0]
	nLabel, sLabel, fProba = probability2label(arProbas, oClasses, nTop = 1)

	# sResults contient le mot prédit
	sResults = "Sign: %s (%.0f%%)" % (sLabel, fProba*100.)
	#print("Mot predit---------------------------" + sResults)
	nCount += 1

			#print(sResults)

		# quit
		#elif key == ord('q'):
		#	break

	# do a bit of cleanup
	oStream.release()
	cv2.destroyAllWindows()

	return sResults


if __name__ == '__main__':
	livedemo()