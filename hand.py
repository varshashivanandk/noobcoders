import cv2
import mediapipe as mp

# Initialize Mediapipe hands detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Setup hands detection with default parameters
hands = mp_hands.Hands(
    max_num_hands=2,  # Track up to two hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame to avoid mirror image
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB as Mediapipe processes RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform hand detection
    results = hands.process(rgb_frame)

    # Check if any hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_type in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Draw landmarks and connections on the frame
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
            
            # Get the hand type (left or right)
            hand_label = hand_type.classification[0].label
            cv2.putText(frame, hand_label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame with detections
    cv2.imshow('Hand Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()