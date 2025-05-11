import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.hand_tracker import HandTracker

tracker = HandTracker()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    position, frame = tracker.get_hand_position(frame)
    if position:
        cv2.circle(frame, position, 10, (0, 255, 0), -1)

    cv2.imshow("Hand Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
tracker.release()
