import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.max_num_hands = max_num_hands

        # Initialize MediaPipe hands solution for hand detection and tracking
        self.mp_hands = mp.solutions.hands
        # Configure the hand-tracking model with specified parameters
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,                    # Max number of hands to detect
            min_detection_confidence=detection_confidence,  # Confidence threshold for initial detection
            min_tracking_confidence=tracking_confidence     # Confidence threshold for tracking
        )
        # Initialize MediaPipe drawing utilities for visualizing landmarks
        self.mp_draw = mp.solutions.drawing_utils

    def get_hand_position(self, frame):
        # Check if the input frame is valid; return None if not
        if frame is None:
            return None, frame

        # Convert the frame from BGR (OpenCV default) to RGB (required by MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame to detect hand landmarks
        results = self.hands.process(frame_rgb)

        # Check if any hand landmarks are detected
        if results.multi_hand_landmarks:
            # Iterate through detected hands (only one expected due to max_num_hands=1)
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the index finger tip landmark (used for paddle control)
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Get frame dimensions to convert normalized coordinates to pixel values
                height, width, _ = frame.shape
                # Convert normalized x, y coordinates (0 to 1) to pixel coordinates
                x = int(index_finger_tip.x * width)
                y = int(index_finger_tip.y * height)

                # Draw a green filled circle at the index finger tip position
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)  # -1 fills the circle

                # Return the (x, y) position and modified frame with the drawn circle
                return (x, y), frame

        # Return None and the original frame if no hands are detected
        return None, frame

    def release(self):
        # Close the MediaPipe hands model to free resources
        self.hands.close()