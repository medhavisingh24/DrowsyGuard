import cv2
import mediapipe as mp
from pygame import mixer

# Initialize alarm sound
mixer.init()
mixer.music.load("alert.wav")  # Alarm file in same folder

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

# Eye aspect ratio function
def eye_aspect_ratio(landmarks, eye_idx):
    A = ((landmarks[eye_idx[1]][0] - landmarks[eye_idx[5]][0])**2 + (landmarks[eye_idx[1]][1] - landmarks[eye_idx[5]][1])**2)**0.5
    B = ((landmarks[eye_idx[2]][0] - landmarks[eye_idx[4]][0])**2 + (landmarks[eye_idx[2]][1] - landmarks[eye_idx[4]][1])**2)**0.5
    C = ((landmarks[eye_idx[0]][0] - landmarks[eye_idx[3]][0])**2 + (landmarks[eye_idx[0]][1] - landmarks[eye_idx[3]][1])**2)**0.5
    return (A+B)/(2.0*C)

# MediaPipe eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

# Open webcam
cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20
counter = 0

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

        # Calculate EAR
        leftEAR = eye_aspect_ratio(landmarks, LEFT_EYE)
        rightEAR = eye_aspect_ratio(landmarks, RIGHT_EYE)
        ear = (leftEAR + rightEAR) / 2.0

        # Show EAR on frame
        cv2.putText(frame, f"EAR: {ear:.2f}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        if ear < EAR_THRESHOLD:
            counter += 1
            cv2.putText(frame, "DROWSY!", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
            if counter >= CONSEC_FRAMES:
                mixer.music.play()
        else:
            counter = 0
            mixer.music.stop()

    cv2.imshow("Driver Drowsiness Detection", frame)

    # Press q or ESC to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
