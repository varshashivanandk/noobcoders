**Project Title: Lane Management**
**Team Members:**  Varsha Shivanand K, Prachi Agarwal, Syed Farhan Ahmed
**Technologies Used:** Python, OpenCV, AI-integrated Cameras
**Project Overview:**
The Lane Management System is an AI-based surveillance solution designed to detect unsafe or unauthorized lane changes using real-time video processing. The system leverages flash detection, hand gesture recognition, and number plate extraction to monitor driver behavior and enforce lane discipline.

**Key Features:**
🚦 **1. Flash Detection**
Detects sudden changes in light intensity — such as flashes from vehicle headlamps or cameras — by analyzing frame-by-frame pixel brightness.

Implements a dynamic thresholding mechanism to adapt to varying ambient lighting conditions.

Differentiates between:

Valid scenarios: Left flash + left-hand signal or right flash + right-hand signal (no action taken).

Invalid scenarios: Mismatched flash and hand signals, triggering a capture.

✋ **2. Hand Gesture Detection**
Continuously captures frames to recognize static hand signals using:

Contour detection

Convex hull and convexity defects to determine the number of extended fingers or signal patterns.

Assists in validating driver intentions when switching lanes.

🚘 **3. Number Plate Recognition**
Detects vehicle number plates in real-time using Haar Cascade classifiers.

Captures and saves an image of the vehicle (including the number plate) to local storage if unauthorized behavior is detected.

Bounding rectangles are drawn around detected number plates for visual confirmation.

**Common System Capabilities:**
**Real-Time Video Monitoring:** Uses OpenCV to stream and process video from an AI-enabled camera.

**Adjustable Sensitivity:** Detection parameters (e.g., scale factor, minNeighbors) can be fine-tuned for different lighting and traffic environments.

**Selfie Capture Logic:** The system captures the full view of the car (what the camera sees) when a rule violation occurs.

**Technological Highlights:**
**Language:** Python

**Libraries:** OpenCV (Computer Vision)

**Hardware:** AI-integrated camera with lane boundary detection and object tracking capabilities

**Application:** Traffic monitoring, lane discipline enforcement, violation logging

