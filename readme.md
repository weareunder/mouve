# Hand Gesture Control

This project implements hand gesture control using computer vision techniques and the Mediapipe library. It allows you to control various actions such as scrolling, volume adjustment, and cursor movement using hand gestures captured from a webcam.

## Features

- Hand detection and tracking: The system uses the Mediapipe library to detect and track the user's hand in real-time.
- Gesture recognition: It recognizes different hand gestures based on the positions and movements of the fingers.
- Scroll control: You can scroll up and down by making specific hand gestures.
- Volume control: Adjust the system volume by moving your hand up and down.
- Cursor control: Control the cursor movement on the screen using hand gestures.

## Getting Started

### Prerequisites

- Python 3.7 or above
- OpenCV
- Mediapipe
- PyAutoGUI

### Installation

1. Clone the repository:
2. Install the required Python packages:
    `pip install -r requirements.txt`

### Usage

1. Run the `app.py` script:
python app.py

2. The script will open a live feed from your webcam and start detecting hand gestures. Follow the instructions displayed on the screen to control various actions.

### Customization

- Constants such as camera resolution and gesture recognition thresholds can be adjusted in the `constants.toml` file.
- Additional gestures and corresponding actions can be added by modifying the `handle_scroll`, `handle_volume`, and `handle_cursor` functions in the script.
