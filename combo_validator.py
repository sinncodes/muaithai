import cv2
import numpy as np
import time
import joblib
import mediapipe as mp
from collections import deque
import pygame
pygame.mixer.init()

CORRECT_SOUND_PATH = "sounds/correct.wav"

def play_sound():
    pygame.mixer.music.load(CORRECT_SOUND_PATH)
    pygame.mixer.music.play()

model = joblib.load("lr_model.pkl")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False)

landmarks_to_use = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def extract_features_and_angles(landmarks):
    coords = [[landmarks.landmark[idx].x,
               landmarks.landmark[idx].y,
               landmarks.landmark[idx].z] for idx in landmarks_to_use]
    flat = [c for point in coords for c in point]

    left_elbow = calculate_angle(coords[4], coords[2], coords[0])
    right_elbow = calculate_angle(coords[5], coords[3], coords[1])
    left_knee = calculate_angle(coords[10], coords[8], coords[6])
    right_knee = calculate_angle(coords[11], coords[9], coords[7])

    angles = [
        left_elbow,
        calculate_angle(coords[2], coords[0], coords[6]),   #left shoulder
        calculate_angle(coords[0], coords[6], coords[8]),   #left hip
        calculate_angle(coords[6], coords[8], coords[10]),  #left knee
        right_elbow,
        calculate_angle(coords[3], coords[1], coords[7]),   #right shoulder
        calculate_angle(coords[1], coords[7], coords[9]),   #right hip
        calculate_angle(coords[7], coords[9], coords[11]),  #right knee
    ]

    joint_map = {
        "jab": left_elbow,
        "cross": right_elbow,
        "lelbow": left_elbow,
        "relbow": right_elbow,
        "lknee": left_knee,
        "rknee": right_knee,
        "lkick": left_knee,
        "rkick": right_knee,
    }

    return flat + angles, joint_map

def get_camera_stream():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open the camera")
        return None
    return cap

def validate_combo(combo, confidence_threshold=0.76):
    cap = get_camera_stream()
    if not cap:
        print("No camera could be opened")
        return

    buffer = deque(maxlen=15)
    predicted_sequence = []
    last_detection_time = time.time()
    last_prompted_strike = None  #to avoid replaying the same cue sound

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, None, fx=1.5, fy=1.5)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        current_pred = "idle"
        person_detected = results.pose_landmarks is not None

        if person_detected:
            last_detection_time = time.time()

            features, joint_map = extract_features_and_angles(results.pose_landmarks)
            features_scaled = scaler.transform(np.array(features).reshape(1, -1))

            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features_scaled)[0]
                boosted = probs.copy()

                top_idx = np.argmax(boosted)
                top_label = encoder.inverse_transform([top_idx])[0]
                top_conf = boosted[top_idx]

                #boost only if angle matches
                boost = 0
                angle = joint_map.get(top_label, None)
                if top_label == "jab" and angle and angle >= 160:
                    boost = 0.37
                elif top_label == "cross" and angle and angle >= 160:
                    boost = 0.37
                elif top_label == "lelbow" and angle and angle <= 70:
                    boost = 0.37
                elif top_label == "relbow" and angle and angle <= 70:
                    boost = 0.37
                elif top_label == "lknee" and angle and angle <= 90:
                    boost = 0.37
                elif top_label == "rknee" and angle and angle <= 90:
                    boost = 0.37
                elif top_label == "lkick" and angle and angle >= 150:
                    boost = 0.39
                elif top_label == "rkick" and angle and angle >= 150:
                    boost = 0.39

                boosted[top_idx] += boost
                boosted /= boosted.sum()
                top_idx = np.argmax(boosted)
                top_label = encoder.inverse_transform([top_idx])[0]
                top_conf = boosted[top_idx]

                print(f"Predicted: {top_label} ({top_conf:.2f} confidence)")

                if top_conf >= confidence_threshold and top_label != "idle":
                    current_pred = top_label
            else:
                current_pred = encoder.inverse_transform(model.predict(features_scaled))[0]
                print(f"Predicted (no proba): {current_pred}")

            buffer.append(current_pred)
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            #play sound
            if len(predicted_sequence) < len(combo):
                next_strike = combo[len(predicted_sequence)]
                if next_strike != last_prompted_strike:
                    try:
                        pygame.mixer.music.load(f"sounds/{next_strike}.mp3")
                        pygame.mixer.music.play()
                        last_prompted_strike = next_strike
                    except Exception as e:
                        print(f"Couldn't play the sound: {e}")

            #combo matching
            if len(buffer) == buffer.maxlen:
                most_common = max(set(buffer), key=buffer.count)
                next_expected = combo[len(predicted_sequence)] if len(predicted_sequence) < len(combo) else None

                if most_common == next_expected:
                    predicted_sequence.append(most_common)
                    play_sound()
                    last_prompted_strike = None  

                    if predicted_sequence == combo:
                        predicted_sequence = []

        if not person_detected and time.time() - last_detection_time > 10:
            print("No person detected for 10 seconds. Exiting.")
            break

        #overlay info
        cv2.putText(frame, "Target Combo: " + "->".join(combo), (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
        cv2.putText(frame, "Your Combo: " + "->".join(predicted_sequence), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow("MuAIthai - Combo Validator", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()