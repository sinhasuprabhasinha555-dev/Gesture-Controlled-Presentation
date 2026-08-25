# Gesture-Controlled Presentation System

A computer-vision-based presentation controller that allows users
to navigate PDF presentations using hand gestures in real time.

## Features

- Real-time hand tracking using MediaPipe
- Gesture-based slide navigation
- One finger → Next slide
- Two fingers → Previous slide
- Open palm → Neutral
- Gesture stabilization to reduce accidental actions
- Cooldown mechanism to prevent repeated commands
- Real-time slide tracking
- PDF presentation control using PyAutoGUI

## Technologies

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Project Structure

Gesture-Controlled-Presentation/
│
├── src/
├── controller/
├── evaluation/
├── tests/
├── utils/
├── assets/
├── gesture_presentation.py
├── test_controller.py
├── requirements.txt
├── README.md
└── .gitignore

## Installation

Clone the repository:

git clone <repository-url>

Create a virtual environment:

python -m venv venv

Activate it:

Windows:
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Usage

Run:

python gesture_presentation.py

Then open a PDF presentation and use the supported gestures
to navigate between slides.

## Gesture Controls

| Gesture | Action |
|---|---|
| One finger | Next slide |
| Two fingers | Previous slide |
| Open palm | Neutral |
| Fist | Neutral |

## How It Works

Webcam
↓
OpenCV
↓
MediaPipe Hand Tracking
↓
Finger Detection
↓
Gesture Classification
↓
Gesture Stabilization
↓
Presentation Controller
↓
PDF Presentation

## Future Improvements

- Virtual laser pointer
- Swipe-based navigation
- Improved gesture recognition
- Presentation timer
- Gesture accuracy evaluation
- More robust performance under different lighting conditions

## Author

Suprabha Sinha