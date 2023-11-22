import cv2
import numpy as np
import Mediapipetools as mpt
import pyautogui as pg
import autopy

# ----------------------------------------------------------------
# preview screen resolution
wCam, hCam = 640, 480
# ----------------------------------------------------------------
# variables declarations
frameR = 100
smoothening = 7

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = mpt.handDetector(maxHands=1)
wScr, hScr = pg.size()

while True:
    success, img = cap.read()  # capture the image
    img = detector.findHands(img)  # Detect the hands
    lmList, bbox = detector.findPosition(img)  # Find position (x,y,z) of each landmarks

    if len(lmList) != 0:  # if a hand is detected
        x1, y1 = lmList[8][1:]  # x,y position of index finger
        x2, y2 = lmList[12][1:]  # x,y position of middle finger

        fingers = detector.fingersUp()  # list fingers facing up or down
        #############################################
        # finger[0] == 1 -> thumb facing up
        # finger[0] == 0 -> thumb facing down
        # finger[1] == 1 -> index finger facing up
        # finger[1] == 0 -> index finger facing down
        # finger[2] == 1 -> middle finger facing up
        # finger[2] == 0 -> middle finger facing down
        # finger[3] == 1 -> ring finger facing up
        # finger[3] == 0 -> ring finger facing down
        # finger[4] == 1 -> pinky finger facing up
        # finger[4] == 0 -> pinky finger facing down
        #############################################
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 210), 2)
        #################################################################################################################
        # Curser movement
        # Index finger facing up and rest is facing down
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR),
                           (0, wScr))  # Equivalent position of x1 from the range 'frameR, wCam-frameR' in 0 to wScr
            y3 = np.interp(y1, (frameR, hCam - frameR),
                           (0, hScr))  # Equivalent position of y1 from the range 'frameR, hCam-frameR' in 0 to hScr

            clocX = plocX + (x3 - plocX) / smoothening  # Current x coordinate
            clocY = plocY + (y3 - plocY) / smoothening  # Current y coordinate

            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        #################################################################################################################
        # Left click
        # Index finger and middle finger is facing up and rest is facing down
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:

            length, img, lineInfo = detector.findDistance(8, 12, img)
            # length have the distance between tip of index an middle finger
            # img have the captured image of hand
            # lineInfo have the x,y positions of index finger, middle finger and their midpoint
            # if distance between tip of index finger and middle finger is less than 40px
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()  # Mouse left click
                print("Left Click")
        #################################################################################################################
        # Three finger right click
        #  Index finger, middle finger and ring finger facing up rest facing down
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            length3, img, lineInfo = detector.findDistance(8, 16, img)
            if length3 < 40:
                pg.click(button='right')
                print("Right Click")
        #################################################################################################################
        # Close current working window
        # All fingers except pinky finger facing down
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            print("Close window in 5 sec")
            pg.PAUSE = 5
            pg.hotkey('alt', 'f4')
            pg.PAUSE = 5
        #################################################################################################################
        # Scroll
        # Index finger and thimb facing down rest are facing up
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            length3, img, lineInfo = detector.findDistance(20, 12, img)
            # print(length3)
            if length3 < 80:
                pg.scroll(-20)
                print("Scrolling down")
                pg.PAUSE = 0.1
            else:
                pg.scroll(20)
                print("Scrolling up")
                pg.PAUSE = 0.1


    cv2.imshow("Image", img)  # Preview the image
    cv2.waitKey(1)  # Waits for a key event infinitely



