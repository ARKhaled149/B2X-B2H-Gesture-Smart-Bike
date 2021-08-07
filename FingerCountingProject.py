import cv2
import time
import os
from PIL import Image
import HandTrackingModule as htm
from serial import Serial
import serial
import numpy as np
ser = serial.Serial(port='/dev/ttyACM0', baudrate= 9600)
sqr_img = 600
wCam, hCam = sqr_img, sqr_img
x11 = 250
x22 = 350
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon = 0.25)
tipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) > 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        x1,y1,katana = 0,0,0
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
                x1+= lmList[tipIds[id]][1]
                y1+= lmList[tipIds[id]][2]
                katana+=1
                
            else:
                fingers.append(0)
        # [fingers.append(1) if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else fingers.append(0) for id in range(1, 5)]
        x1 = x1 /(katana+0.001)
        y1 = y1 /(katana+0.001)
        totalFingers = fingers.count(1)
        # totalFingers = np.count_nonzero(np.array(fingers))
        # print(x1,y1)
        factor = 20/(sqr_img/2)
        # print(factor)
        mean = x1 - sqr_img//2
        print(mean)
        angle_value = int(mean * factor)
        if angle_value >= 1:
            angle_value = f"+{angle_value:02}"
        elif angle_value <= -1:
            angle_value = f"-{abs(angle_value):02}"
        print(angle_value)
        if totalFingers == 5:
            s = f"5,{angle_value}\n"
            ser.write(s.encode('utf-8'))
        else:
            s = f"0,{angle_value}\n"
            ser.write(s.encode('utf-8'))
        # elif totalFingers == 0:
        #     if x1 > x11 and x1 < x22:
        #         ser.write(b"3,+00\n")
        #     elif x1 < x11:
        #         ser.write(b"3,-15\n")
        #     elif x1 > x22:
        #         ser.write(b"3,+15\n")
        ser.flushInput()
        ser.flush()
        ser.flushOutput()
        # cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
ser.close()