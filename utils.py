import cv2

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
