from cvzone.SerialModule import SerialObject

import serial
import time
import cv2
import time
import numpy as np
import Hand_Tracking_Module_ as htm
import math

arduino = SerialObject("COM5")

##############################
wCam, hCam = 640, 480
##############################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

while True:

    Success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPositon(img)

    if lmList:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]   # accessing landmark 4 x and y values
        x2, y2 = lmList[8][1], lmList[8][2]

        # getting the center of the line
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # making circle around them
        cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)

        # create line between them
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
        # circle between the line
        cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

        # now we have to find the lenght between these point, we uses hypotenues function of math lib
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # our hand range 30 - 230
        # volume range -65 - 0
        # so we have to convert the lenght to vol

        angle = np.interp(length, [30, 200], [0, 255])
        print(length, int(angle))

        arduino.sendData([angle])

        if length < 35:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Img", img)
    key = cv2.waitKey(1)

    if key == 80 or key == 113:
        break

arduino.close()

print("Code Completed")
