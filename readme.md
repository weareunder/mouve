# Hand Gesture Control

This project implements hand gesture control using computer vision techniques and the Mediapipe library. It allows you to control various actions such as scrolling, volume adjustment, and cursor movement using hand gestures captured from a webcam.

## Features

- Hand detection and tracking: The system uses the Mediapipe library to detect and track the user's hand in real-time.
- Gesture recognition: It recognizes different hand gestures based on the positions and movements of the fingers.
- ...

## Getting Started
install `anaconda` on mac and run `source ~/.zshrc`  to reload your paths file:

`<https://repo.anaconda.com/archive/Anaconda3-2023.07-0-MacOSX-arm64.pkg>`

### Prerequisites

- Python 3.7 or above
- OpenCV
- Mediapipe
- PyAutoGUI

### Installation

1. Clone the repository:
2. Create a new virtual env in your terminal
   `conda create -n dl python=3.10 anaconda`
3. activate the env
   `conda activate dl`
4. Install the required Python packages:
    `pip install -r requirements.txt`

### Usage

1. Run the `app.py` script:
python app.py

2. The script will open a live feed from your webcam and start detecting hand gestures. Follow the instructions displayed on the screen to control various actions.

### Customization

- Constants such as camera resolution and gesture recognition thresholds can be adjusted in the `constants.toml` file.
- Additional gestures and corresponding actions can be added by modifying the `handle_scroll`, `handle_volume`, and `handle_cursor` functions in the script.

### core functionalities
if you're diving in, you'll want to understand the heart of our system, controller.py.

### instances: `handmajor` and `handminor`
these instances use deep learning (dl) to accurately gauge and interpret hand gestures captured via the camera. they set the stage for more advanced functionalities in the future.

### method: `start`
this method is responsible for the core operations:
1. effective video frame handling: it discards empty frames intelligently.
2. advanced image processing: optimizes images for gesture analysis.
3. dynamic gesture management: recognizes and adapts to various gestures effectively.
4. deeper into the process
5. once start identifies hand landmarks, it collaborates with handmajor and handminor to understand the gestures being performed.

### gesture classification
the `set_finger_state` method helps in distinguishing the current state of the hand.

### gesture execution
the `get_gesture` method retrieves and directs the recognized gesture for appropriate control.

### gestures we support
the system currently supports the following gestures:

1. left click
2. right click
3. drag and drop
4. double click
5. neutral
6. scroll
