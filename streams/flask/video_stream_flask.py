# Import necessary libraries
import sys
from flask import Flask, render_template, Response
import cv2
import numpy as np
# Initialize the Flask app
app = Flask(__name__)

# This works with normal cameras, but not the Realsense depth stream. Need to figure out how to get hold of that data.
camera = None
overlay = True
port = 5000
orientation = 0  # How many times to rotate image by 90 degrees


def gen_frames():
    frame_count = 0
    while True:
        frame_count = frame_count + 1
        success, frame = camera.read()  # read the camera frame
        np.rot90(frame, orientation)
        if not success:
            break
        else:
            if overlay:
                frame = draw_overlay(frame, f"Marvin Status\nFrames: {frame_count}")
            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    # Default route just to provide a simple test page
    return "Nothing here"


@app.route('/video_feed')
def video_feed():
    # Use the co-routine to generate and send image frames
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def draw_overlay(frame, overlay_text):
    # Frames are ndarray objects, [y, x, blue, green, red]
    frame = draw_crosshair(frame)
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 1.2
    color = (0, 255, 0)
    thickness = 1
    line_height = 15

    height = len(frame)

    lines = overlay_text.split("\n")
    orig = height - len(lines)*line_height
    for line in lines:
        frame = cv2.putText(frame, line, (10, orig), font, fontScale, color, thickness, cv2.LINE_AA)
        orig = orig + line_height
    return frame


def draw_crosshair(frame):
    width = len(frame)
    height = len(frame[0])

    width_cen = int(width/2)
    height_cen = int(height/2)

    # Main cross hair lines
    cv2.line(frame, (height_cen, 0), (height_cen, width), (0, 255, 0), 1)
    cv2.line(frame, (0, width_cen), (height, width_cen), (0, 255, 0), 1)

    minor_tick = 5
    major_tick = 10

    # Minor ticks
    for i in range(20, height, 40):
        cv2.line(frame, (i, width_cen-minor_tick), (i, width_cen+minor_tick), (0, 255, 0), 1)
    for i in range(20, width, 40):
        cv2.line(frame, (height_cen-minor_tick, i), (height_cen+minor_tick, i), (0, 255, 0), 1)

    # Major ticks
    for i in range(40, height, 40):
        cv2.line(frame, (i, width_cen-major_tick), (i, width_cen+major_tick), (0, 255, 0), 1)
    for i in range(40, width, 40):
        cv2.line(frame, (height_cen-major_tick, i), (height_cen+major_tick, i), (0, 255, 0), 1)
    return frame


if __name__ == "__main__":
    port = int(sys.argv[1])
    camera_number = int(sys.argv[2])
    orientation = int(sys.argv[3]) if len(sys.argv) >= 4 else 0
    overlay = len(sys.argv) >= 5 and sys.argv[4] == "overlay"
    print(f"Port Number {port}; Camera Number {camera_number}; Orientation {orientation}; Overlay? {overlay}")
    camera = cv2.VideoCapture(camera_number)
    app.run(host='0.0.0.0', port=port, debug=False)  # Note: Setting debug to true causes the video capture to fail
