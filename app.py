from flask import Flask, render_template, request, Response, jsonify
from real_time_detection import generate_video_feed, get_current_result, start_detection, stop_detection
from data_collection import  start_video_feed, stop_video_feed, generate_frames

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')



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



# Route for the HTML page
@app.route('/data_collection')
def data_collection():
    return render_template('data_collect.html')









# Real-time detection page
@app.route('/real_time_detection')
def real_time_detection():
    return render_template('real_time_detection.html')

# Video feed for real-time detection
@app.route('/video_feed')
def video_feed():
    return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for getting current detection result
@app.route('/current_result')
def current_result():
    return get_current_result()

# Start and stop detection routes
@app.route('/start', methods=['POST'])
def start():
    return start_detection()

@app.route('/stop', methods=['POST'])
def stop():
    return stop_detection()

if __name__ == '__main__':
    app.run(debug=True)




