# Real-Time Hand Gesture Recognition and Computer Control

A real-time computer vision application that enables users to control selected computer functions using hand gestures captured through a webcam.

The system uses Python, OpenCV, and MediaPipe to detect hand landmarks, recognize predefined finger patterns, and execute computer actions through PyAutoGUI.

## Features

- Real-time webcam-based hand detection.
- Detection of 21 hand landmark points.
- Recognition of predefined finger configurations.
- Media playback and pause control.
- Next-track and previous-track navigation.
- System mute control.
- Continuous volume increase and decrease.
- Gesture stabilization and cooldown mechanisms to help reduce accidental activations.

## Gesture Controls

| Hand Gesture | Action |
|---|---|
| One finger raised | Play / Pause |
| Two fingers raised | Next Track |
| Three fingers raised | Previous Track |
| Four fingers raised | Decrease Volume |
| Five fingers raised | Increase Volume |
| Closed fist | Mute |

The application uses predefined gesture patterns. Refer to `main.py` for the exact gesture detection logic and action mappings.

## Technologies Used

- **Python** — application logic.
- **OpenCV** — webcam access and video-frame processing.
- **MediaPipe** — hand detection and landmark extraction.
- **PyAutoGUI** — computer-control and media commands.
- **NumPy** — numerical operations and supporting computations.

## Project Structure

```text
hand-gesture-recognition/
├── models/
├── main.py
├── requirements.txt
├── README.md
└── statement.md
```

The `models/` directory contains model assets used by the application. Keep the existing model files in their expected locations.

## Requirements

Before running the project, ensure that you have:

- Python installed in a version compatible with the dependencies in `requirements.txt`.
- A working webcam.
- A computer with a supported desktop environment.
- Internet access for installing dependencies.
- Permission to access the webcam and control the required computer functions.

## Installation and Setup

### Step 1: Clone the repository

Open a terminal or command prompt and run:

```bash
git clone https://github.com/rudraporwal8/hand-gesture-recognition.git
```

### Step 2: Navigate to the project directory

```bash
cd hand-gesture-recognition
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install the dependencies

Ensure that `requirements.txt` is present in the project directory, then run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If installation fails, check the Python version and operating-system compatibility of the pinned packages in `requirements.txt`. Avoid randomly upgrading individual packages because computer vision dependencies can have version constraints.

### Step 5: Run the application

From the project root, execute:

```bash
python main.py
```

Allow webcam access if prompted. Position your hand within the camera's field of view and use the supported gestures to trigger computer actions.

### Step 6: Stop the application

Use the exit key or window-closing method implemented in `main.py`. If the application does not close normally, stop the process from the terminal using `Ctrl+C`.

## How the System Works

1. **Video capture:** OpenCV captures frames from the webcam.
2. **Hand detection:** MediaPipe detects the hand and extracts its landmark points.
3. **Finger analysis:** The application evaluates landmark positions to determine finger states.
4. **Gesture recognition:** Predefined finger patterns are matched to supported gestures.
5. **Stabilization:** The program uses stabilization and cooldown logic to reduce accidental activations.
6. **Action execution:** PyAutoGUI sends the corresponding computer-control command.

## Troubleshooting

### Webcam not opening
- Close other applications that may be using the camera.
- Check operating-system camera permissions.
- Verify that the webcam is connected and available.

### Missing Python modules
- Activate the project's virtual environment.
- Run `pip install -r requirements.txt` again.
- Review any package installation errors and confirm Python compatibility.

### Gesture not recognized
- Keep the hand clearly visible within the camera frame.
- Improve lighting and avoid excessive background clutter.
- Ensure that the fingers are positioned clearly according to the supported gesture patterns.

### Media controls not responding
- Confirm that the target media application supports the relevant media commands.
- Check operating-system permissions and the desktop environment.
- Verify that the intended action is mapped correctly in `main.py`.

### Model file errors
- Confirm that the required model assets are present in the `models/` directory.
- Preserve the expected filenames and paths referenced by the source code.

## Limitations

- Recognition depends on camera quality, lighting, and hand visibility.
- Only predefined gestures are supported.
- Computer-control behavior may differ across operating systems and applications.
- The project has not been presented as having a measured recognition-accuracy percentage unless supported by actual testing.

## Future Enhancements

- Customizable gesture-to-action mappings.
- Support for additional gestures and applications.
- Quantitative evaluation of recognition accuracy and response time.
- Improved handling of different lighting conditions and hand orientations.
- A graphical interface for configuring controls.

## Project Statement

Refer to [`statement.md`](statement.md) for the project's problem statement, objectives, proposed solution, scope, and expected outcome.
