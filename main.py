import cv2 as cv
import numpy as np
import module as m
import time
#import RPi.GPIO as GPIO



# Variables
COUNTER = 0
TOTAL_BLINKS = 0
CLOSED_EYES_FRAME = 3
Ear_thresh_low = 0.2
Blink_count = 0
cameraID = 0
a=0
camera = cv.VideoCapture(0)
start_time = time.time() # calculate total program time
blink_timer = time.time () # calculate time of every blink
while True:
   # FRAME_COUNTER += 1
    ret, frame = camera.read()

         # converting frame into Gry image.
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
           # calling the face detector funciton
    image, face = m.faceDetector(frame, grayFrame)
    if face is not None:

        # calling landmarks detector funciton.
        image, PointList = m.faceLandmakDetector(frame, grayFrame, face, False)
        RightEyePoint = PointList[36:42]
        LeftEyePoint = PointList[42:48]
        leftRatio, topMid, bottomMid = m.blinkDetector(LeftEyePoint)
        rightRatio, rTop, rBottom = m.blinkDetector(RightEyePoint)
        cv.circle(image, topMid, 2, m.YELLOW, -1)
        cv.circle(image, bottomMid, 2, m.YELLOW, -1)

        blinkRatio = (leftRatio + rightRatio)/2

        if blinkRatio > 4:
            COUNTER += 1
            cv.putText(image, f'Blink', (50, 50),m.fonts, 1, m.LIGHT_BLUE, 2)
        else:
            if COUNTER > CLOSED_EYES_FRAME:
                TOTAL_BLINKS += 1
                blink_timer +=1
                COUNTER = 0
                blink_timer = 0
        cv.putText(image, f'Total Blinks: {TOTAL_BLINKS}', (50, 80),
                   m.fonts, 1.2, m.LIGHT_BLUE, 2)
        mask, pos, color = m.EyeTracking(frame, grayFrame, RightEyePoint)
        
        
        if blink_timer !=1:
                    #stop the motor
             for a in range (5):
                    cv. putText(image, "Motor is stoped", (50, 50), m.fonts, 1,m.BLACK, 2) 
        else :
             for a in range (10):
                    cv. putText(image, "Motor is started", (50, 50), m.fonts, 1,m.BLACK, 2) 
                   
        cv.putText(image, f'Total Blinks: {TOTAL_BLINKS}', (50, 80),
                   m.fonts, 1.2, m.LIGHT_BLUE, 2)
              
        # draw background as line where we put text.
        cv.line(image, (30, 90), (100, 90), color[0], 30)

           # writing text on above line
        cv.putText(image, f'{pos}', (35, 95), m.fonts, 0.6, color[1], 2)

        # showing the frame on the screen
        cv.imshow('Frame', image)
    else:
        cv.imshow('Frame', frame)

    key = cv.waitKey(1)

    # if q is pressed on keyboard: quit
    if key == ord('q'):
        #GPIO.cleanup()
        break
# closing the camera
camera.release()
cv.destroyAllWindows()