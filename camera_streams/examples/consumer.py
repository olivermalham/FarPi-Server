import cv2
from flask import Flask, render_template, Response
from ..marvin_array_feed import MarvinArrayFeed

# Initialize the Flask app
app = Flask(__name__)

port = 5000

marvin_image_stream = MarvinArrayFeed(stream="image_feed")


def fetch_frame():
    while True:
        image = marvin_image_stream.next_array()

        ret, buffer = cv2.imencode('.jpg', image)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    # Default route just to provide a simple test page
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Use the co-routine to generate and send image frames
    return Response(fetch_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print(f"Port Number {port}")
    app.run(host='0.0.0.0', port=port, debug=False)  # Note: Setting debug to true causes the video capture to fail
