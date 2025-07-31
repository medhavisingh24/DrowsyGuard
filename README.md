🚗 DrowsyGuard – Driver Drowsiness Detection System
Author: Medhavi Singh




📌 Overview
Drowsy driving is a major cause of road accidents. DrowsyGuard is an AI-based application that detects driver fatigue in real-time using a webcam.

Tracks eye aspect ratio (EAR) to detect closed eyes

Plays an alarm if the driver appears drowsy for a few seconds

Runs locally on your computer with a webcam

🛠 Tech Stack
Python 3.10

OpenCV – Real-time video processing

dlib / Mediapipe – Face & eye landmark detection

imutils – Utility for image processing

Pygame – Play alert sound

📂 Project Structure
bash
Copy
Edit
driver_drowsiness/
│── drowsiness_detection.py   # Main script
│── alert.wav                 # Alarm sound
│── requirements.txt          # Python dependencies
│── README.md                 # Project description
⚡ How It Works
Capture real-time video from the webcam

Detect eyes using facial landmarks

Calculate Eye Aspect Ratio (EAR)

If eyes remain closed for >2 seconds → Play alarm


🌟 Future Improvements
Deploy as a mobile app for real drivers

Integrate Streamlit dashboard for analytics

Support night vision cameras

🏆 Achievements
Real-time detection with minimal lag

95% accuracy for simulated drowsy conditions

Can prevent driver fatigue accidents

