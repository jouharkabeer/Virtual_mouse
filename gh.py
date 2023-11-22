import cv2
import numpy as np
import Mediapipetools as htm
import pyautogui as pg
import autopy

wCam, hCam = 640, 480
frameR = 100
smoothening = 7
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pg.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR),(0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR),(0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pg.click()
                print("Left Click")
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            length3, img, lineInfo = detector.findDistance(8, 16, img)
            if length3 < 40:
                pg.click(button='right')
                print("Right Click")
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            print("Close window in 5 sec")
            pg.PAUSE = 5
            pg.hotkey('alt', 'f4')
            pg.PAUSE = 5
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            length3, img, lineInfo = detector.findDistance(20, 12, img)
            if length3 < 100:
                pg.scroll(-20)
                print("Scrolling down")
                pg.PAUSE = 0.1
            else:
                pg.scroll(20)
                print("Scrolling up")
                pg.PAUSE = 0.1
    cv2.imshow("Image", img)
    cv2.waitKey(1)