import cv2
import mediapipe as mp


# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# Finger detection function
def count_fingers(hand_landmarks):

    fingers = 0

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers += 1

    # Index finger
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
        fingers += 1

    # Middle finger
    if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
        fingers += 1

    # Ring finger
    if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y:
        fingers += 1

    # Pinky
    if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y:
        fingers += 1

    return fingers


# Start webcam
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        print("Could not access webcam.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)

    fingers = 0

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Count fingers
            fingers = count_fingers(hand_landmarks)

    # Display finger count
    cv2.putText(
        frame,
        f"Fingers: {fingers}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Display gesture
    if fingers == 0:
        gesture = "FIST"
    elif fingers == 1:
        gesture = "ONE FINGER"
    elif fingers == 2:
        gesture = "TWO FINGERS"
    elif fingers == 5:
        gesture = "OPEN PALM"
    else:
        gesture = "UNKNOWN"

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Show camera
    cv2.imshow("Gesture Detector", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
hands.close()