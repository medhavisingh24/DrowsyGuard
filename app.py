import streamlit as st
import cv2
import tempfile

st.title("🚗 DrowsyGuard - Driver Drowsiness Demo")

st.write("This demo shows how our system detects driver drowsiness using a pre-recorded video.")

uploaded_file = st.file_uploader("Upload a demo video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save video to a temp file
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)

    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB", use_container_width=True)  # ✅ Fixed here

    cap.release()
    st.success("✅ Video playback complete!")
else:
    st.info("Please upload a video to start the demo.")
