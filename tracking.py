import cv2
import mediapipe as mp
import time


class handDetector():
    """A class for detecting and tracking hands using MediaPipe library.

    Args:
        mode (bool, optional): Whether to detect multiple hands. Defaults to False.
        maxHands (int, optional): Maximum number of hands to detect. Defaults to 2.
        detectionCon (float, optional): Minimum confidence threshold for hand detection. Defaults to 0.5.
        trackCon (float, optional): Minimum confidence threshold for hand tracking. Defaults to 0.5.
    """
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """Detects hands in the given image and optionally draws landmarks.

        Args:
            img (numpy.ndarray): Input image.
            draw (bool, optional): Whether to draw landmarks on the image. Defaults to True.

        Returns:
            numpy.ndarray: Image with hand landmarks (if draw=True).
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True, color=(255, 0, 255), z_axis=False):
        """Finds the positions of hand landmarks in the given image.

        Args:
            img (numpy.ndarray): Input image.
            handNo (int, optional): Hand index to retrieve landmarks from. Defaults to 0.
            draw (bool, optional): Whether to draw landmarks on the image. Defaults to True.
            color (tuple, optional): Color of the drawn landmarks. Defaults to (255, 0, 255).
            z_axis (bool, optional): Whether to include the z-axis coordinate of landmarks. Defaults to False.

        Returns:
            list: List of hand landmarks' positions.
        """
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                if not z_axis:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                elif z_axis:
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), round(lm.z, 3)
                    lmList.append([id, cx, cy, cz])

                if draw:
                    cv2.circle(img, (cx, cy), 5, color, cv2.FILLED)

        return lmList