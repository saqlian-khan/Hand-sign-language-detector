
from flask import Flask, render_template, Response, request, jsonify
import cv2
import os

app = Flask(__name__)

# Initialize the video capture
camera = None
video_feed_active = False

# Function to start video feed
def start_video_feed():
    global camera, video_feed_active
    if not video_feed_active:
        camera = cv2.VideoCapture(0)  # Start camera capture
        video_feed_active = True

# Function to stop video feed
def stop_video_feed():
    global camera, video_feed_active
    if video_feed_active:
        camera.release()  # Release the camera
        video_feed_active = False

# Video streaming generator function
def generate_frames():
    global camera
    while video_feed_active:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to handle starting the video feed
@app.route('/start_video_feed', methods=['POST'])
def start_feed():
    start_video_feed()
    return jsonify({'status': 'Video feed started'})

# Route to handle stopping the video feed
@app.route('/stop_video_feed', methods=['POST'])
def stop_feed():
    stop_video_feed()
    return jsonify({'status': 'Video feed stopped'})

# Route for video feed display
@app.route('/video_feed1')
def video_feed1():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to collect data for a specific class
@app.route('/collect_data', methods=['POST'])
def collect_data():
    data = request.get_json()
    class_id = data.get('class_id')
    # Collect frames logic (adjust directory paths as necessary)
    if class_id is not None:
        folder_path = f'data/class_{class_id}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Save the current frame
        for i in range(100):  # Example: save 10 frames
            success, frame = camera.read()
            if success:
                frame_path = os.path.join(folder_path, f'frame_{i}.jpg')
                cv2.imwrite(frame_path, frame)
        return jsonify({'message': f'Data for class {class_id} collected successfully.'})
    else:
        return jsonify({'message': 'Class ID not provided.'}), 400

# Route for the HTML page
@app.route('/data_collection')
def index():
    return render_template('data_collect.html')

if __name__ == '__main__':
    app.run(debug=True)










            




