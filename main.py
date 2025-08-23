import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp

cap=cv2.VideoCapture(0)
time.sleep(2)
while cap.isOpened():

        # Read feed
    while(True):
    # Capture frame-by-frame
       ret, frame = cap.read()
       if ret is None:
         print("Errorcamera")
         break
        # Our operations on the frame come here

        # Display the resulting frame
       else:
        cv2.imshow('frame',frame)
       if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()