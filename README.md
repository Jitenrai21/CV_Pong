
# CV Pong - Hand Gesture Controlled Pong Game

CV Pong is a computer vision-based Pong game that allows players to control paddles using real-time hand gestures detected through a webcam. It uses MediaPipe for hand tracking and Pygame for game rendering and mechanics.

## Features

- Real-time hand tracking using MediaPipe
- Index finger gesture control mapped to paddles
- Dual-hand control: left and right frame division
- Automatic opponent control fallback if no right-hand detected
- Webcam feed as live background
- Smooth paddle movement with gesture input
- Modular code structure for easy testing and scalability

## Folder Structure

```

CV_PONG/
├── utils/
│   ├── hand_tracker.py       # Handles webcam & hand detection (MediaPipe)
│   ├── game.py               # Pong game logic (pygame or OpenCV window)  
│   ├── utils.py              # Helper functions (e.g., coordinate mapping)
│   └── multi_hand_tracker.py
│
├── tests/
│   ├── multi_hand_tracker_test.py
│   └── hand_tracker_test.py
│
├── game.py                   # main file after integration
├── game-Multiplayer.py
├── requirements.txt          # List of dependencies
└── README.md                 # Project overview and instructions
```

## Requirements

- Python 3.7+
- pip (Python package manager)

## Dependencies

Install required packages using:

```

pip install -r requirements.txt

```

`requirements.txt` should include:
- opencv-python
- pygame
- mediapipe
- numpy

## How to Run

1. Clone the repository:

```

git clone https://github.com/Jitenrai21/CV_Pong

```

2. Run the game:

```

python main\game-Multiplayer.py

```

3. Ensure your webcam is connected and permissions are granted.

## Controls

- Show your **left hand** in the **left half** of the screen to control the **left paddle**.
- Show your **right hand** in the **right half** of the screen to control the **right paddle**.
- If no right-hand is detected, the right paddle is controlled by the computer.

## Development Notes

- The hand tracking logic is encapsulated in `multi_hand_tracker.py` for modularity.
- The tracking module was independently tested using `multi_hand_tracker_test.py`.
- Frame dimensions are mapped for coordinate transformation.
- Paddle movement is smoothed to avoid jitter due to hand detection noise.
- The frame is horizontally flipped for a natural mirror effect.

## Future Enhancements

- Gesture-based controls for pause, resume, and restart
- Multiplayer support via networked webcams
- UI overlays for better feedback and instructions

## License

This project is open-source and available under the MIT License.

---

Developed by JitenraiJR21
```

