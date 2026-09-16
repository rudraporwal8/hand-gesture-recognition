import cv2
import mediapipe as mp
import time
import pyautogui

# -----------------------------
# MediaPipe setup
# -----------------------------
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/hand_landmarker.task"
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# Finger counting
# -----------------------------
def count_fingers(hand):
    fingers = []

    # Thumb
    if hand[4].x > hand[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index
    fingers.append(1 if hand[8].y < hand[6].y else 0)

    # Middle
    fingers.append(1 if hand[12].y < hand[10].y else 0)

    # Ring
    fingers.append(1 if hand[16].y < hand[14].y else 0)

    # Pinky
    fingers.append(1 if hand[20].y < hand[18].y else 0)

    return fingers


# -----------------------------
# Gesture recognition
# -----------------------------
def recognize_gesture(fingers):

    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"

    elif fingers == [0, 1, 0, 0, 0]:
        return "ONE"

    elif fingers == [0, 1, 1, 0, 0]:
        return "TWO"

    elif fingers == [0, 1, 1, 1, 0]:
        return "THREE"

    elif fingers == [0, 1, 1, 1, 1]:
        return "FOUR"

    elif fingers == [1, 1, 1, 1, 1]:
        return "FIVE"

    return "UNKNOWN"


# -----------------------------
# Actions
# -----------------------------
def execute_action(gesture):

    if gesture == "ONE":
        pyautogui.press("playpause")
        return "PLAY / PAUSE"

    elif gesture == "TWO":
        pyautogui.press("nexttrack")
        return "NEXT TRACK"

    elif gesture == "THREE":
        pyautogui.press("prevtrack")
        return "PREVIOUS TRACK"

    elif gesture == "FIST":
        pyautogui.press("volumemute")
        return "MUTE"

    return ""


# -----------------------------
# Start camera
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera")
    exit()

print("Camera started!")
print("Show your hand to control the computer.")
print("Press Q to quit.")


# -----------------------------
# Gesture stability
# -----------------------------
previous_gesture = "UNKNOWN"
stable_gesture = "UNKNOWN"

gesture_counter = 0
REQUIRED_FRAMES = 5


# -----------------------------
# Volume control
# -----------------------------
last_volume_change = 0

# Time between volume changes
VOLUME_INTERVAL = 0.15


# -----------------------------
# Other actions
# -----------------------------
last_action_time = 0
ACTION_COOLDOWN = 1.0

last_action = "None"


# -----------------------------
# FPS
# -----------------------------
previous_time = 0

timestamp = 0


# -----------------------------
# MediaPipe
# -----------------------------
with HandLandmarker.create_from_options(options) as landmarker:

    while True:

        success, frame = cap.read()

        if not success:
            print("Could not read camera")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp
        timestamp += 33

        # Detect hand
        result = landmarker.detect_for_video(
            mp_image,
            timestamp
        )

        gesture = "NO HAND"
        fingers = [0, 0, 0, 0, 0]

        # -----------------------------
        # Hand detected
        # -----------------------------
        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            # Count fingers
            fingers = count_fingers(hand)

            # Recognize gesture
            gesture = recognize_gesture(fingers)

            # Draw landmarks
            h, w, _ = frame.shape

            for landmark in hand:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

            # -----------------------------
            # Bounding box
            # -----------------------------
            x_coordinates = [
                int(lm.x * w) for lm in hand
            ]

            y_coordinates = [
                int(lm.y * h) for lm in hand
            ]

            x_min = max(min(x_coordinates) - 20, 0)
            x_max = min(max(x_coordinates) + 20, w)

            y_min = max(min(y_coordinates) - 20, 0)
            y_max = min(max(y_coordinates) + 20, h)

            cv2.rectangle(
                frame,
                (x_min, y_min),
                (x_max, y_max),
                (255, 0, 0),
                2
            )

            # -----------------------------
            # Stable gesture detection
            # -----------------------------
            if gesture == previous_gesture:

                gesture_counter += 1

            else:

                gesture_counter = 0
                previous_gesture = gesture

            if gesture_counter >= REQUIRED_FRAMES:

                if stable_gesture != gesture:

                    stable_gesture = gesture

                    # -----------------------------
                    # One-time actions
                    # -----------------------------
                    current_time = time.time()

                    if (
                        gesture not in ["FOUR", "FIVE"]
                        and
                        current_time - last_action_time
                        > ACTION_COOLDOWN
                    ):

                        action = execute_action(gesture)

                        if action:
                            last_action = action
                            last_action_time = current_time

        else:

            stable_gesture = "NO HAND"
            gesture_counter = 0
            previous_gesture = "NO HAND"

        # ==================================================
        # CONTINUOUS VOLUME CONTROL
        # ==================================================

        current_time = time.time()

        if stable_gesture == "FIVE":

            if current_time - last_volume_change >= VOLUME_INTERVAL:

                pyautogui.press("volumeup")

                last_volume_change = current_time

                last_action = "VOLUME UP"

        elif stable_gesture == "FOUR":

            if current_time - last_volume_change >= VOLUME_INTERVAL:

                pyautogui.press("volumedown")

                last_volume_change = current_time

                last_action = "VOLUME DOWN"

        # -----------------------------
        # FPS calculation
        # -----------------------------
        current_time = time.time()

        if previous_time != 0:

            fps = 1 / (current_time - previous_time)

        else:

            fps = 0

        previous_time = current_time

        # -----------------------------
        # Display information
        # -----------------------------

        cv2.putText(
            frame,
            f"Gesture: {stable_gesture}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Fingers: {sum(fingers)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Action: {last_action}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "FIVE = Volume Up",
            (20, 190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "FOUR = Volume Down",
            (20, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Q = Quit",
            (20, 260),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Show camera
        cv2.imshow(
            "Hand Gesture Control",
            frame
        )

        # Quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()