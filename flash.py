import cv2
import numpy as np

def capture_frame(video_source=0):
    # Capture video from the specified source (default is webcam)
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return None

    return frame

def detect_flash(frame):
    # Convert the frame to grayscale for flash detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to detect bright areas (potential phone flash)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Split the frame into left and right halves
    height, width = thresh.shape
    left_half = thresh[:, :width // 2]
    right_half = thresh[:, width // 2:]

    # Check if there are any non-zero pixels in the left and right halves
    left_flash = np.any(left_half)
    right_flash = np.any(right_half)

    return left_flash, right_flash

def main():
    # Capture video from the webcam in a loop
    video_source = 0
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Flip the frame horizontally to correct the inversion
        frame = cv2.flip(frame, 1)

        # Detect flash
        left_flash, right_flash = detect_flash(frame)

        # Clear previous text
        overlay_frame = frame.copy()

        # Display the result
        if left_flash:
            print("Flash detected on the left side!")
            cv2.putText(overlay_frame, "Left Flash ON", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        if right_flash:
            print("Flash detected on the right side!")
            cv2.putText(overlay_frame, "Right Flash ON", (overlay_frame.shape[1] // 2 + 10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Show the frame with overlay
        cv2.imshow('Flash Detection', overlay_frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video source and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()