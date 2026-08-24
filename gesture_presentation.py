import cv2
import mediapipe as mp
import time

from src.presentation_controller import PresentationController
from src.slide_tracker import SlideTracker


# ==========================================
# MediaPipe Setup
# ==========================================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)


# ==========================================
# Finger Detection
# ==========================================

def count_fingers(hand_landmarks, handedness):

    landmarks = hand_landmarks.landmark

    fingers = 0

    # Thumb
    if handedness == "Right":
        if landmarks[4].x < landmarks[3].x:
            fingers += 1
    else:
        if landmarks[4].x > landmarks[3].x:
            fingers += 1

    # Index
    if landmarks[8].y < landmarks[6].y:
        fingers += 1

    # Middle
    if landmarks[12].y < landmarks[10].y:
        fingers += 1

    # Ring
    if landmarks[16].y < landmarks[14].y:
        fingers += 1

    # Pinky
    if landmarks[20].y < landmarks[18].y:
        fingers += 1

    return fingers


# ==========================================
# Gesture Classification
# ==========================================

def get_gesture(fingers):

    if fingers == 1:
        return "NEXT"

    elif fingers == 2:
        return "PREVIOUS"

    elif fingers == 5:
        return "OPEN PALM"

    else:
        return "NEUTRAL"


# ==========================================
# Gesture Stability Settings
# ==========================================

STABLE_FRAMES = 8

candidate_gesture = "NONE"
candidate_count = 0

current_gesture = "NONE"
action_locked = False


# ==========================================
# Create Controllers
# ==========================================

controller = PresentationController(
    cooldown=1.2
)

tracker = SlideTracker(
    total_slides=12
)


# ==========================================
# Execute Gesture
# ==========================================

def execute_gesture(gesture):

    global action_locked

    if gesture == "NEXT":

        if controller.next_slide():

            tracker.next_slide()

            print(
                f"Current: {tracker.get_status()}"
            )

            action_locked = True

            return True

    elif gesture == "PREVIOUS":

        if controller.previous_slide():

            tracker.previous_slide()

            print(
                f"Current: {tracker.get_status()}"
            )

            action_locked = True

            return True

    return False


# ==========================================
# Start Webcam
# ==========================================

cap = cv2.VideoCapture(0)

print()
print("==========================================")
print("   Gesture Controlled Presentation")
print("==========================================")
print()
print("☝️  One finger  = NEXT")
print("✌️  Two fingers = PREVIOUS")
print("✋  Open palm   = NEUTRAL")
print("✊  Fist        = NEUTRAL")
print()
print("Current slide: 1 / 12")
print("Press Q to quit.")
print()


# ==========================================
# Main Loop
# ==========================================

while True:

    success, frame = cap.read()

    if not success:

        print("Could not access webcam.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect hand
    results = hands.process(rgb_frame)

    gesture = "NO HAND"

    # ======================================
    # Hand Detected
    # ======================================

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        # Get handedness
        handedness = (
            results
            .multi_handedness[0]
            .classification[0]
            .label
        )

        # Draw landmarks
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # Count fingers
        fingers = count_fingers(
            hand_landmarks,
            handedness
        )

        # Detect gesture
        gesture = get_gesture(fingers)

        # ==================================
        # Gesture Stability
        # ==================================

        if gesture == candidate_gesture:

            candidate_count += 1

        else:

            candidate_gesture = gesture
            candidate_count = 1

        # ==================================
        # Confirm Stable Gesture
        # ==================================

        if candidate_count >= STABLE_FRAMES:

            current_gesture = gesture

        # ==================================
        # Execute Navigation
        # ==================================

        if (
            current_gesture in ["NEXT", "PREVIOUS"]
            and not action_locked
        ):

            execute_gesture(
                current_gesture
            )

    else:

        # No hand detected
        gesture = "NO HAND"

        candidate_gesture = "NONE"
        candidate_count = 0
        current_gesture = "NONE"

        # Unlock after hand disappears
        action_locked = False


    # ======================================
    # Neutral Gesture Unlock
    # ======================================

    if current_gesture not in [
        "NEXT",
        "PREVIOUS"
    ]:

        action_locked = False


    # ======================================
    # Display Information
    # ======================================

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Stable: {current_gesture}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"{tracker.get_status()}",
        (20, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "1 Finger = NEXT",
        (20, 145),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "2 Fingers = PREVIOUS",
        (20, 175),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Open Palm = NEUTRAL",
        (20, 205),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Q = Quit",
        (20, 235),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # ======================================
    # Show Camera
    # ======================================

    cv2.imshow(
        "Gesture Controlled Presentation",
        frame
    )


    # ======================================
    # Quit
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# Cleanup
# ==========================================

cap.release()

cv2.destroyAllWindows()

hands.close()