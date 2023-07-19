# Hand Gesture Control

This project implements hand gesture control using computer vision techniques and the Mediapipe library. It allows you to control various actions such as scrolling, volume adjustment, and cursor movement using hand gestures captured from a webcam.

## Features

- Hand detection and tracking: The system uses the Mediapipe library to detect and track the user's hand in real-time.
- Gesture recognition: It recognizes different hand gestures based on the positions and movements of the fingers.
- Scroll control: You can scroll up and down by making specific hand gestures.
- Volume control: Adjust the system volume by moving your hand up and down.
- Cursor control: Control the cursor movement on the screen using hand gestures.

## Getting Started

install `anaconda` on mac and run `source ~/.zshrc`  to reload your paths file:

`https://repo.anaconda.com/archive/Anaconda3-2023.07-0-MacOSX-arm64.pkg`

### Prerequisites

- Python 3.7 or above
- OpenCV
- Mediapipe
- PyAutoGUI

### Installation

1. Clone the repository:
2. Create a new virtual env in your terminal

        conda create -n dl python=3.10 anaconda
3. activate the env

        conda activate dl
4. Install the required Python packages:

        pip install -r requirements.txt

### Usage

1. Run the `app.py` script:

        python app.py

2. The script will open a live feed from your webcam and start detecting hand gestures. Follow the instructions displayed on the screen to control various actions.

### Customization

- Constants such as camera resolution and gesture recognition thresholds can be adjusted in the `constants.toml` file.
- Additional gestures and corresponding actions can be added by modifying the `handle_scroll`, `handle_volume`, and `handle_cursor` functions in the script.

#### Additional Steps for macOS M1

If you are using a macOS M1 device, follow these additional steps:

1. Remove the already installed conda environment:

        conda remove -n dl --all

2. Create the conda environment again, this time using the `environment.yml` file:

        conda env create -f environment.yml

3. Once the environment is installed, activate it:

        conda activate dl

4. Run the gesture recognition main file:

        python app.py
