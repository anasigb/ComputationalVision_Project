# Mini Project By: Hanan Egbaria, Majdy Aburia and Anas Egbaria
# USAGE
# python algo.py --video videos/outdoornature.mp4 --frames 150 --verify 20 --sense 1
#All arguments is optional

# import the necessary packages
import argparse
import imutils
import cv2
import numpy

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--video", help="path to the video file")
ap.add_argument("--frames", help="Number of learning frames")
ap.add_argument("--verify", help="Number of frames to verify true motions")
ap.add_argument("--sense", help="sensetivity")
args = vars(ap.parse_args())

#intialize helping vars
c=0
sum1=0
avg1=0
max1=0
min1=0
verifier=0
TextAvg= ''
TextMin= ''
TextMax= ''
TextDif= ''
dif1=0
text = ""
bluredtext= "No Recording"
backgroundmodelingtext="Modeling background..."

#handling arguments
if args.get("frames", None) is None:
 LearningFrames=150
else: 
 LearningFrames = int(args["frames"] )

if args.get("verify", None) is None:
 NumOfFramesToVerify = 20
else:
 NumOfFramesToVerify = int(args["verify"])

if args.get("sense", None) is None:
 sesetivity=1
else:
 sesetivity = int(args["sense"])

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
 cap = cv2.VideoCapture(0)
 time.sleep(0.25)

# otherwise, we are reading from a video file
else:
 cap = cv2.VideoCapture(args["video"])
 
#main analyzing Loop   
 while(1):
  ret, frame = cap.read()
  infoframe=frame
  c=c+1 
  if not ret:
   break

#resize frame
  frame = imutils.resize(frame, width=500)
#blurring pixels to eliminate noised pixels
  bluredframe = cv2.GaussianBlur(frame, (21, 21), 0) 

  frame3colorsavg = (cv2.sumElems(bluredframe)[0] + cv2.sumElems(bluredframe)[1] + cv2.sumElems(bluredframe)[2]) / 3
  
  if c==1:
   min1 = frame3colorsavg
   max1 = frame3colorsavg
  
  if c <= LearningFrames:
   sum1 = sum1 + frame3colorsavg
   if frame3colorsavg < min1:
    min1 = frame3colorsavg

   if frame3colorsavg > max1:
    max1 = frame3colorsavg


  if c == LearningFrames:
   avg1 = sum1 / LearningFrames
   dif1= max(max1 - avg1, avg1 - min1)

   TextAvg= 'background pixels average = ' + str(avg1)
   TextMin= 'min = ' + str(min1)
   TextMax= 'max = ' + str(max1)
   TextDif= 'maximal deviation = ' + str(dif1)
   backgroundmodelingtext="finished modeling background!"
 
  if c >= LearningFrames:
   if abs(frame3colorsavg - avg1)*sesetivity > dif1:
    verifier = verifier + 1

   if verifier > 0 and verifier < NumOfFramesToVerify and text != "Recording..":
    bluredtext = "maybe , verifing.."

   if verifier >= NumOfFramesToVerify:
    text = "Recording.."
    bluredtext = "Recording.."
   
   if abs(frame3colorsavg - avg1)*sesetivity <= dif1 and verifier > 0:
    verifier = verifier - 1

   if verifier == 0:
    text = ""
    bluredtext = "No Recording"
  
# to show the text 
  cv2.putText(frame, text, (10, 30),
   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
  


  cv2.putText(bluredframe, bluredtext, (10, 20),
   cv2.FONT_HERSHEY_SIMPLEX, 0.65, (102, 255, 255), 2)
  
  cv2.putText(bluredframe, backgroundmodelingtext, (10, 100),
   cv2.FONT_HERSHEY_SIMPLEX, 0.65, (102, 255, 255), 2)

  cv2.putText(bluredframe, TextAvg, (10, 50),
   cv2.FONT_HERSHEY_SIMPLEX, 0.65, (102, 255, 102), 2)

  cv2.putText(bluredframe, TextDif, (10, 70),
   cv2.FONT_HERSHEY_SIMPLEX, 0.65, (102, 255, 102), 2)    
  
  cv2.imshow("Camera Feed", frame)
  cv2.imshow("blured frame", bluredframe)

  # quit function
  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
   break
  
 print(c)
 cap.release()
 cv2.destroyAllWindows()
