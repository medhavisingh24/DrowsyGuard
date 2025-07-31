import streamlit as st
import cv2
import tempfile
import time

st.title("🚗 DrowsyGuard - Driver Drowsiness Detection Demo")

uploaded_file = st.file_uploader("Upload a demo video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded video to a temp file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ---------------------------
        # Fake Drowsiness Detection (replace with EAR logic later)
        ear = 0.2  # example EAR value
        status_text = "Drowsy" if ear < 0.25 else "Alert"
        color = (0, 0, 255) if status_text == "Drowsy" else (0, 255, 0)

        # Show status on video
        cv2.putText(frame, f"Status: {status_text}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        # ---------------------------

        # Convert BGR to RGB for Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB", use_container_width=True)

        # Add small delay for smoother playback
        time.sleep(0.03)

    cap.release()
    st.success("✅ Video playback complete!")
else:
    st.info("Please upload a video to start the demo.")
