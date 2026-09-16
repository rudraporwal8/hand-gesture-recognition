# Hand Gesture Recognition and Computer Control ✋

This is a real-time Computer Vision project that lets you control some basic computer functions using hand gestures.

The project uses a webcam to detect my hand, identify which fingers are open, and then recognize the gesture. The recognized gesture is mapped to an action such as increasing the volume, decreasing the volume, playing/pausing media, changing tracks, or muting the sound.

## What the project does

The webcam continuously captures video and the program looks for a hand in each frame.

Once a hand is detected, MediaPipe gives 21 landmark points for the hand. I use these points to check which fingers are open and then match the finger combination with one of the gestures defined in the program.

For example:

- 1 finger → Play / Pause
- 2 fingers → Next Track
- 3 fingers → Previous Track
- 4 fingers → Volume Down
- 5 fingers → Volume Up
- Fist → Mute

For volume control, the action keeps happening while the gesture is being shown. So if I keep showing 5 fingers, the volume keeps increasing. Similarly, showing 4 fingers keeps decreasing the volume.

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

### What each one is used for

**OpenCV**  
Used to access the webcam and process the video frames.

**MediaPipe**  
Used to detect the hand and get its 21 landmark points.

**PyAutoGUI**  
Used to send the media control commands to the computer.

**NumPy**  
Used as a dependency for the computer vision libraries.

---

## How it works

The basic process of the project is:

```text
Webcam
   ↓
Capture Video Frame
   ↓
Detect Hand
   ↓
Get 21 Hand Landmarks
   ↓
Check Finger Positions
   ↓
Recognize Gesture
   ↓
Perform Computer Action
