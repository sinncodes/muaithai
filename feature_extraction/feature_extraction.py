import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import os
import re

#this won't work as there is no more raw data folder

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)  #for live prediction

#landmarks
important_landmarks = {
    11: "left_shoulder", 12: "right_shoulder",
    13: "left_elbow", 14: "right_elbow",
    15: "left_wrist", 16: "right_wrist",
    23: "left_hip", 24: "right_hip",
    25: "left_knee", 26: "right_knee",
    27: "left_ankle", 28: "right_ankle"
}
landmark_indices = list(important_landmarks.keys())

def extract_pose_features(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if results.pose_landmarks:
        row = []
        for idx in landmark_indices:
            lm = results.pose_landmarks.landmark[idx]
            row.extend([lm.x, lm.y, lm.z])  
        return row
    return None

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def extract_joint_angles_from_features(features_row):
    row = np.array(features_row).reshape(12, 3)

    #landmark references
    ls, rs = row[0], row[1]
    le, re = row[2], row[3]
    lw, rw = row[4], row[5]
    lhip, rhip = row[6], row[7]
    lk, rk = row[8], row[9]
    la, ra = row[10], row[11]

    angles = [
        calculate_angle(lw, le, ls),      #left elbow
        calculate_angle(le, ls, lhip),    #left shoulder
        calculate_angle(ls, lhip, lk),    #left hip
        calculate_angle(lhip, lk, la),    #left knee
        calculate_angle(rw, re, rs),      #right elbow
        calculate_angle(re, rs, rhip),    #right shoulder
        calculate_angle(rs, rhip, rk),    #right hip
        calculate_angle(rhip, rk, ra)     #right knee
    ]
    return angles

#labels for weighting
punch_labels = {"jab", "cross", "lupper", "rupper", "lelbow", "relbow"}
kick_labels = {"lkick", "rkick", "lknee", "rknee"}
idle_labels = {"idle"}

def apply_feature_weighting(features, angles, label):
    arm_weight, leg_weight = 1.0, 1.0

    if label in punch_labels:
        leg_weight = 0.2
    elif label in kick_labels:
        arm_weight = 0.2
    elif label in idle_labels:
        arm_weight = leg_weight = 0.3

    row = np.array(features).reshape(12, 3)  # 3D

    arm_indices = [0, 1, 2, 3, 4, 5]
    leg_indices = [6, 7, 8, 9, 10, 11]

    weighted_landmarks = []
    for idx, (x, y, z) in enumerate(row):
        if idx in arm_indices:
            weighted_landmarks.extend([x * arm_weight, y * arm_weight, z * arm_weight])
        elif idx in leg_indices:
            weighted_landmarks.extend([x * leg_weight, y * leg_weight, z * leg_weight])

    weighted_angles = [
        angles[0] * arm_weight,  #left elbow
        angles[1] * arm_weight,  #left shoulder
        angles[2] * leg_weight,  #left hip
        angles[3] * leg_weight,  #left knee
        angles[4] * arm_weight,  #right elbow
        angles[5] * arm_weight,  #right shoulder
        angles[6] * leg_weight,  #right hip
        angles[7] * leg_weight   #right knee
    ]

    return weighted_landmarks + weighted_angles

def process_folder(folder_path, output_raw_csv, output_angles_csv, output_weighted_csv, max_frames=5):
    raw_rows, angles_rows, weighted_rows = [], [], []

    for file in os.listdir(folder_path):
        label = re.sub(r"\d+", "", os.path.splitext(file)[0])
        path = os.path.join(folder_path, file)
        cap = cv2.VideoCapture(path)

        frame_count = 0
        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            features = extract_pose_features(frame)
            if features:
                angles = extract_joint_angles_from_features(features)
                weighted_features = apply_feature_weighting(features, angles, label)

                raw_rows.append(features + [label])                   #x, y, z
                angles_rows.append(features + angles + [label])      #x, y, z + angles
                weighted_rows.append(weighted_features + [label])    #weighted

                frame_count += 1
        cap.release()

    pd.DataFrame(raw_rows).to_csv(output_raw_csv, index=False, header=False)
    pd.DataFrame(angles_rows).to_csv(output_angles_csv, index=False, header=False)
    pd.DataFrame(weighted_rows).to_csv(output_weighted_csv, index=False, header=False)

#paths
video_folder = "data"
output_raw_csv = "pose_data_features_only.csv"
output_angles_csv = "pose_data_with_angles.csv"
output_weighted_csv = "pose_data_with_angles_weighted.csv"

if __name__ == "__main__":
    process_folder(video_folder, output_raw_csv, output_angles_csv, output_weighted_csv)