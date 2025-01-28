import pickle
import cv2
import mediapipe as mp
import numpy as np
from flask import jsonify

# Load the pre-trained model (pickle file)
try:
    with open('./model.p', 'rb') as f:
        model_dict = pickle.load(f)
    model = model_dict['model']
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Labels for predictions
labels_dict = {0: 'Hello ', 1: 'bad', 2: 'yejas',3:'peace',4:'good'}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

# Global variables to manage results and detection state
current_result = "None"  
detection_active = False  

def generate_video_feed():
    global current_result, detection_active
    cap = cv2.VideoCapture(0)  # Capture from the default webcam

    if not cap.isOpened():
        print("Error: Unable to open video source.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture video frame.")
            break

        # Only perform detection when the detection is active
        if detection_active:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw the hand landmarks using a single color (green)
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(225, 0, 0), thickness=2, circle_radius=3),  # Hand landmarks
                        mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2)  # Hand connections
                    )

                    # Prepare data for prediction
                    data_aux = []
                    x_ = []
                    y_ = []

                    for landmark in hand_landmarks.landmark:
                        x_.append(landmark.x)
                        y_.append(landmark.y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                    if model:
                        try:
                            # Make prediction using the model
                            prediction = model.predict([np.asarray(data_aux)])
                            predicted_character = labels_dict.get(int(prediction[0]), "Unknown")
                            current_result = predicted_character
                        except Exception as e:
                            current_result = "Error in prediction"
                            print(f"Prediction error: {e}")

                        # Calculate bounding box for the hand
                        x1 = int(min(x_) * frame.shape[1]) - 10
                        y1 = int(min(y_) * frame.shape[0]) - 10
                        x2 = int(max(x_) * frame.shape[1]) + 10
                        y2 = int(max(y_) * frame.shape[0]) + 10

                        # Draw bounding box and the prediction
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)
                        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)

        # Encode the frame into JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            print("Error encoding frame.")
            break

        # Yield the encoded frame as part of the video feed
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    cap.release()


def get_current_result():
    global current_result
    return jsonify({'result': current_result})

def start_detection():
    global detection_active
    detection_active = True
    return jsonify({"status": "detection started"})

def stop_detection():
    global detection_active
    detection_active = False
    return jsonify({"status": "detection stopped"})























