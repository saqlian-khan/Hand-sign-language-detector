import cv2
import os
# from flask import jsonify

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

cap = None
number_of_classes = 3
dataset_size = 100
class_id = 0  # Default class for data collection
collecting = False
frame = None  # Current video frame


def start_video_capture():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible!")
  

def stop_video_capture():
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()



def collect_data(class_id):
    global collecting, frame
    data_path = os.path.join(DATA_DIR, str(class_id))
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print(f"Directory created: {data_path}")

    counter = 0
    while counter < dataset_size and collecting:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video frame.")
            break

        if not ret:
            break
        # Save the current frame
        cv2.imwrite(os.path.join(DATA_DIR, str(class_id), '{}.jpg'.format(counter)), frame)
        counter += 1

    return "Data collection for class {} completed.".format(class_id)


def generate_frames():
    global cap, frame
    while collecting is True:
        if cap is None:
            continue
        ret, frame = cap.read()
        if not ret:
            break
        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Create a streamable HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')














