import cv2
import time
import math
import numpy as np
import pyautogui
from subprocess import call
from AppKit import NSSound
from ctypes import cast, POINTER
import toml
import tracking

# Load constants from a TOML file
constants = toml.load("constants.toml")
hmin = constants["hmin"]
hmax = constants["hmax"]
color = constants["color"]
tipIds = constants["tipIds"]

# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(3, constants["wCam"])
cap.set(4, constants["hCam"])

pTime = 0

# Create a hand detector object
detector = tracking.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

def handle_scroll(mode, img, lmList, fingers):
    """Handles scroll actions.

    Args:
        mode (str): Current mode.
        img (numpy.ndarray): Input image.
        lmList (list): List of hand landmarks.
        fingers (list): Fingers' states.

    Returns:
        tuple: Updated mode and active state.
    """
    putText(mode)
    cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
    
    if fingers == [0, 1, 0, 0, 0]:
        # putText(mode='U', loc=(200, 455), color=(0, 255, 0))
        pyautogui.scroll(300)
    elif fingers == [0, 1, 1, 0, 0]:
        # putText(mode='Down', loc=(200, 455), color=(0, 0, 255))
        pyautogui.scroll(-300)
    elif fingers == [0, 0, 0, 0, 0]:
        return 'N', 0

    return mode, 1

def handle_volume(mode, img, lmList, fingers):
    """Handles volume control.

    Args:
        mode (str): Current mode.
        img (numpy.ndarray): Input image.
        lmList (list): List of hand landmarks.
        fingers (list): Fingers' states.

    Returns:
        tuple: Updated mode and active state.
    """
    putText(mode)
    if len(lmList) != 0:
        if fingers[-1] == 1:
            return 'N', 0

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), color, 3)
        cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [hmin, hmax], [0, 100])
        volBar = np.interp(vol, [0, 100], [400, 150])
        volPer = np.interp(vol, [0, 100], [0, 100])
        vol = int(vol)
        call([f"osascript -e 'set volume output volume {vol}'"], shell=True)

        if length < 50:
            cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)

        cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
        cv2.rectangle(img, (30, int(volBar)), (55, 400), (215, 255, 127), cv2.FILLED)

    return mode, 1

def handle_cursor(mode, img, lmList, fingers):
    """Handles cursor control.

    Args:
        mode (str): Current mode.
        img (numpy.ndarray): Input image.
        lmList (list): List of hand landmarks.
        fingers (list): Fingers' states.

    Returns:
        tuple: Updated mode and active state.
    """
    putText(mode)
    cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

    if fingers[1:] == [0, 0, 0, 0]:  # thumb excluded
        return 'N', 0
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        w, h = pyautogui.size()
        X = int(np.interp(x1, [110, 620], [0, w - 1]))
        Y = int(np.interp(y1, [20, 350], [0, h - 1]))
        cv2.circle(img, (lmList[8][1], lmList[8][2]), 7, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 255, 0), cv2.FILLED)  # thumb

        if X % 2 != 0:
            X = X - X % 2
        if Y % 2 != 0:
            Y = Y - Y % 2
        print(X, Y)
        pyautogui.moveTo(X, Y)

        if fingers[0] == 0:
            cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)  # thumb
            pyautogui.click()

    return mode, 1

# Main loop
if __name__ == '__main__':
    mode = 'N'
    active = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # img = np.zeros_like(img)

        fingers = []

        if len(lmList) != 0:
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0 - 1]][1]:
                if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            elif lmList[tipIds[0]][1] < lmList[tipIds[0 - 1]][1]:
                if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            if (fingers == [0, 0, 0, 0, 0]) and (active == 0):
                mode = 'N'
            elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and (active == 0):
                mode = 'Scroll'
                active = 1
            elif (fingers == [1, 1, 0, 0, 0]) and (active == 0):
                mode = 'Volume'
                active = 1
            elif (fingers == [1, 1, 1, 1, 1]) and (active == 0):
                mode = 'Cursor'
                active = 1

        if mode == 'Scroll':
            mode, active = handle_scroll(mode, img, lmList, fingers)
        elif mode == 'Volume':
            mode, active = handle_volume(mode, img, lmList, fingers)
        elif mode == 'Cursor':
            mode, active = handle_cursor(mode, img, lmList, fingers)

        cTime = time.time()
        fps = 1 / ((cTime + 0.01) - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (480, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Hand LiveFeed', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        def putText(mode, loc=(250, 450), color=(0, 255, 255)):
            cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_SIMPLEX,
                        2, color, 3)
