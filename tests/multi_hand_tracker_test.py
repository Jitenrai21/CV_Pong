import cv2
import sys
import os

# Add utils directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.multi_hand_tracker import HandTracker

# Initialize hand tracker (max 2 hands)
hand_tracker = HandTracker(max_num_hands=2)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam could not be opened.")
    sys.exit()

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip horizontally

    if not ret:
        print("Error: Failed to read frame from webcam.")
        break

    # Get hand data and annotated frame
    hand_data, annotated_frame = hand_tracker.get_hand_positions(frame)

    # Process each detected hand
    for i, (x, y) in enumerate(hand_data):
        label = "Left" if i == 0 else "Right"

        # Draw circle
        cv2.circle(annotated_frame, (int(x), int(y)), 10, (0, 255, 0), -1)

        # Label the point
        # cv2.putText(annotated_frame, f"{label} ({int(x)}, {int(y)})",
        #             (int(x) + 15, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX,
        #         0.6, (255, 255, 255), 2)

    cv2.imshow('Index Finger Tracker', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hand_tracker.release()
cap.release()
cv2.destroyAllWindows()
