import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import numpy as np

st.title("🚗 DrowsyGuard")

uploaded_file = st.file_uploader("Upload a driving video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded video to a temp file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)

    # Initialize Mediapipe
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [263, 387, 385, 362, 380, 373]

    def eye_aspect_ratio(landmarks, eye_idx):
        A = np.linalg.norm(np.array(landmarks[eye_idx[1]]) - np.array(landmarks[eye_idx[5]]))
        B = np.linalg.norm(np.array(landmarks[eye_idx[2]]) - np.array(landmarks[eye_idx[4]]))
        C = np.linalg.norm(np.array(landmarks[eye_idx[0]]) - np.array(landmarks[eye_idx[3]]))
        return (A + B) / (2.0 * C)

    EAR_THRESHOLD = 0.25
    CONSEC_FRAMES = 10
    counter = 0

    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = []
            for lm in results.multi_face_landmarks[0].landmark:
                h, w, _ = frame.shape
                landmarks.append((lm.x * w, lm.y * h))

            leftEAR = eye_aspect_ratio(landmarks, LEFT_EYE)
            rightEAR = eye_aspect_ratio(landmarks, RIGHT_EYE)
            ear = (leftEAR + rightEAR) / 2.0

            # Display EAR on the frame
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Drowsiness detection
            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= CONSEC_FRAMES:
                    cv2.putText(frame, "DROWSY!", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
            else:
                counter = 0

        # Show frame in Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame)
