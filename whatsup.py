import cv2
import numpy as np
import mediapipe as mp
import os
from datetime import datetime

# Initialize Mediapipe hands detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Setup hands detection with default parameters
hands = mp_hands.Hands(
    max_num_hands=2,  # Track up to two hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Function to detect flash
def detect_flash(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    height, width = thresh.shape
    left_half = thresh[:, :width // 2]
    right_half = thresh[:, width // 2:]
    left_flash = np.any(left_half)
    right_flash = np.any(right_half)
    return left_flash, right_flash

# Function to take a photo
def take_photo(frame):
    # Create directory for photos if it doesn't exist
    directory = "photos"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Flip the frame horizontally to save it inverted
    inverted_frame = cv2.flip(frame, 1)
    # Create a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_path = os.path.join(directory, f"photo_{timestamp}.jpg")
    # Save the inverted frame as a photo
    cv2.imwrite(photo_path, inverted_frame)
    print(f"Photo taken and saved as: {photo_path}")

def main():
    # Open the webcam
    video_source = 0
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    # Dictionaries to store detection statuses
    flash_status = {
        "left_flash": False,
        "right_flash": False
    }
    hand_status = {
        "left_hand_detected": False,
        "right_hand_detected": False
    }
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Flip the frame to correct the mirror effect
        frame = cv2.flip(frame, 1)
        
        # Step 1: Detect flash
        left_flash, right_flash = detect_flash(frame)
        flash_status["left_flash"] = left_flash
        flash_status["right_flash"] = right_flash
        
        # Step 2: Perform hand detection after flash detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        # Reset the hand status before updating it
        hand_status["left_hand_detected"] = False
        hand_status["right_hand_detected"] = False
        
        # Step 3: Update hand detection status
        if results.multi_hand_landmarks:
            for hand_landmarks, hand_type in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Draw landmarks and connections on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Get the hand type (left or right)
                hand_label = hand_type.classification[0].label
                if hand_label == "Left":
                    hand_status["left_hand_detected"] = True
                elif hand_label == "Right":
                    hand_status["right_hand_detected"] = True
                
                # Display the hand type on the frame
                cv2.putText(frame, hand_label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Step 4: Display flash detection status on the frame
        if flash_status["left_flash"]:
            print("Flash detected on the left side!")
            cv2.putText(frame, "Left Flash ON", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if flash_status["right_flash"]:
            print("Flash detected on the right side!")
            cv2.putText(frame, "Right Flash ON", (frame.shape[1] // 2 + 10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Check conditions for taking a photo
        if (hand_status["left_hand_detected"] and hand_status["right_hand_detected"]):
            print("Both hands detected; continuing the loop.")
        elif (hand_status["left_hand_detected"] and flash_status["right_flash"]) or \
             (hand_status["right_hand_detected"] and flash_status["left_flash"]):
            print("Taking a photo!")
            take_photo(frame)

        # Show the frame with all overlays
        cv2.imshow('Flash and Hand Detection', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Print the final detection statuses
    print("Final Flash Status:", flash_status)
    print("Final Hand Status:", hand_status)

if __name__ == '__main__':
    main()