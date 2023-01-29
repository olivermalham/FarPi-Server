# Import necessary libraries
import sys
import numpy as np
from flask import Flask, render_template, Response
import cv2

# Initialize the Flask app
app = Flask(__name__)

port = 5000


def draw_overlay(frame, overlay_text, frames):
    # Frames are ndarray objects, [y, x, blue, green, red]
    frame = draw_crosshair(frame)
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 1.2
    color = (0, 255, 0)
    thickness = 1
    line_height = 15

    frame = cv2.putText(frame, f"{frames}", (100, 100), font, 4, (0, 255, 255), 2, cv2.LINE_AA)

    height = len(frame)

    lines = overlay_text.split("\n")
    orig = height - len(lines) * line_height
    for line in lines:
        frame = cv2.putText(frame, line, (10, orig), font, fontScale, color, thickness, cv2.LINE_AA)
        orig = orig + line_height
    return frame


def draw_crosshair(frame):
    width = len(frame)
    height = len(frame[0])

    width_cen = int(width/2)
    height_cen = int(height/2)

    # Main cross-hair lines
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


def gen_depth_frames():
    frames = 0
    while True:
        frames = frames + 1
        img = np.full((480, 640, 3), 96, dtype=np.uint8)
        img = draw_overlay(img, "Depth datafeed", frames)

        ret, buffer = cv2.imencode('.jpg', img)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_colour_frames():
    frames = 0
    while True:
        frames = frames + 1
        img = np.full((480, 640, 3), 128, dtype=np.uint8)
        img = draw_overlay(img, "Mock Marvin Video Feed", frames)

        ret, buffer = cv2.imencode('.jpg', img)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_ir_frames():
    frames = 0
    while True:
        frames = frames + 1
        img = np.full((480, 640, 3), 64, dtype=np.uint8)
        img = draw_overlay(img, "IR datafeed", frames)

        ret, buffer = cv2.imencode('.jpg', img)

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
    return Response(gen_colour_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/depth_feed')
def depth_feed():
    # Use the co-routine to generate and send image frames
    return Response(gen_depth_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ir_feed')
def ir_feed():
    # Use the co-routine to generate and send image frames
    return Response(gen_ir_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    port = 9876  # int(sys.argv[1])
    print(f"Port Number {port}")

    # Start streaming
    app.run(host='0.0.0.0', port=port, debug=False)  # Note: Setting debug to true causes the video capture to fail
