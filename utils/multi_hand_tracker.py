import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        self.max_num_hands = max_num_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def get_hand_positions(self, frame):
        if frame is None:
            return [], frame

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        hand_positions = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                height, width, _ = frame.shape
                x = int(index_finger_tip.x * width)
                y = int(index_finger_tip.y * height)
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                hand_positions.append((x, y))
        return hand_positions, frame

    def release(self):
        self.hands.close()