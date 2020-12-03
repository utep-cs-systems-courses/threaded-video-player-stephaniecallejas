#!/usr/bin/env python3

import cv2
import os
import time
import numpy as np
from threading import Thread
from QueueE import QueueE

"""Lab 3 Threaded Video Player
   Stephanie Calljeas
   This lab assignment was created with the use of demos provided by the professors. 
   The lab involves first getting the frames from a video. The frames will be enconded and
   then stored into a queue. From the first queue we will be dequeing and decoding the frames
   into a photo and changing the photo from color to gray. The gray photo will be encoded and 
   stored into a second queue. Finally we will dequeue from the second queue each frame, 
   decode it to be a photo and display every 42 milliseconds a gray photo/frame into the
   screen. Important elements of the lab are that 3 threads will be used to concurrently
   process and trasform the frames. Semaphores will be used to avoid processing more than 
   10 frames at the time in each queue. 
"""

clipFileName = "clip.mp4"
capacity = 10

readFramesQueue = QueueE(capacity)
grayFramesQueue = QueueE(capacity)


def extractFrames(clipFileName, readFramesQueue):
    vidcap = cv2.VideoCapture(clipFileName) #Getting the video
    count = 0
    success,image = vidcap.read()           #Reading first frame
    print(f'Reading frame {count} {success}')
    while success and count < 72:
        
        #Get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)
        readFramesQueue.enqueue(jpgImage)
        success,image = vidcap.read()       #Read next frame
        print(f'Reading frame {count}')
        count += 1
    readFramesQueue.enqueue(None)           #Adding a None to the end of the queue
    print("Video Extraction completed")     #For the stopping point


def convertToGrayScale(readFramesQueue, grayFramesQueue):
    # initialize frame count
    count = 0

    # get the first jpg encoded frame from the queue
    inputFrame = readFramesQueue.dequeue()

    while inputFrame is not None and count < 72:
        print(f'Converting frame {count}')

        #Decode to convert back into an image
        image = cv2.imdecode(inputFrame, cv2.IMREAD_UNCHANGED)
        
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Encode the image again to store into the next queue
        success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)
        
        #change it to enqueue into the grayFramesQueue
        grayFramesQueue.enqueue(jpgImage)
        count += 0 

        #Dequeue the next jpg encoded frame
        inputFrame = readFramesQueue.dequeue()
        
    grayFramesQueue.enqueue(None) #Again add None for the stopping point
    print("Video has been converted to gray")
    
def displayFrames(grayFramesQueue):
    # initialize frame count
    count = 0
    
    # load the first gray frame
    frame = grayFramesQueue.dequeue() 

    while frame is not None:
        print(f'Displaying frame {count}')

        # Decode back the frame into an image
        image = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
        
        # Display the frame/image in a window called "Video"
        cv2.imshow('Video', image)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

        # Read the next jpg encoded frame
        frame = grayFramesQueue.dequeue()

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()


#Creation and start of the 3 threads which will handle the methods
extractThread = Thread(target = extractFrames, args = (clipFileName, readFramesQueue)).start()
greyFramesThread = Thread(target = convertToGrayScale, args = (readFramesQueue, grayFramesQueue)).start()
displayThread = Thread(target = displayFrames, args = (grayFramesQueue,)).start()