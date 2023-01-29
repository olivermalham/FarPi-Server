# Import necessary libraries
import sys
import pyrealsense2.pyrealsense2 as rs
import numpy as np
from flask import Flask, render_template, Response
import cv2

# Initialize the Flask app
app = Flask(__name__)

port = 5000

# Configure depth and color streams
context = rs.context()
pipeline = rs.pipeline(context)
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)


def draw_overlay(frame, colour, overlay_text, origin=None):
    # Frames are ndarray objects, [y, x, blue, green, red]
    # font = cv2.FONT_HERSHEY_PLAIN
    # font_scale = 1.2
    # thickness = 1
    # line_height = 15
    #
    # height = len(frame)
    #
    # lines = overlay_text.split("\n")
    # if origin is None:
    #     origin = (10, height - len(lines) * line_height)
    #
    # for line in lines:
    #     frame = cv2.putText(frame, line, origin, font, font_scale, colour, thickness, cv2.LINE_AA)
    #     origin = origin + line_height
    return frame


def draw_crosshair(frame, colour, box=0):
    # width = len(frame)
    # height = len(frame[0])
    #
    # width_cen = int(width / 2)
    # height_cen = int(height / 2)
    # half_box = box / 2
    #
    # # Main crosshair lines
    # cv2.line(frame, (height_cen, 0), (height_cen, width_cen - half_box), colour, 1)
    # cv2.line(frame, (height_cen, width_cen + half_box), (height_cen, width), colour, 1)
    #
    # cv2.line(frame, (0, width_cen), (height_cen - half_box, width_cen), colour, 1)
    # cv2.line(frame, (height_cen + half_box, width_cen), (height, width_cen), colour, 1)
    #
    # minor_tick = 5
    # major_tick = 10
    #
    # # Minor ticks
    # for i in range(20, height, 40):
    #     cv2.line(frame, (i, width_cen - minor_tick), (i, width_cen + minor_tick), colour, 1)
    # for i in range(20, width, 40):
    #     cv2.line(frame, (height_cen - minor_tick, i), (height_cen + minor_tick, i), colour, 1)
    #
    # # Major ticks
    # for i in range(40, height, 40):
    #     cv2.line(frame, (i, width_cen - major_tick), (i, width_cen + major_tick), colour, 1)
    # for i in range(40, width, 40):
    #     cv2.line(frame, (height_cen - major_tick, i), (height_cen + major_tick, i), colour, 1)
    return frame


def gen_depth_frames():
    frame_count = 0
    while True:
        frame_count = frame_count + 1
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_color_mapped = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), cv2.COLORMAP_JET)

        depth_color_mapped = draw_overlay(depth_color_mapped, (255, 255, 255), f"Frame No. {frame_count}")
        depth_color_mapped = draw_crosshair(depth_color_mapped, (255, 255, 255), box=40)

        ret, buffer = cv2.imencode('.jpg', depth_color_mapped)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_colour_frames():
    frame_count = 0
    while True:
        frame_count = frame_count + 1
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        colour_frame = frames.get_color_frame()
        # Convert images to numpy arrays
        colour_image = np.asanyarray(colour_frame.get_data())
        colour_image = draw_overlay(colour_image, (0, 255, 0), f"Frame No. {frame_count}")
        colour_image = draw_crosshair(colour_image, (0, 255, 0))

        ret, buffer = cv2.imencode('.jpg', colour_image)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_ir_frames():
    frame_count = 0
    while True:
        frame_count = frame_count + 1
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        ir_frame = frames.get_infrared_frame()
        # Convert images to numpy arrays
        ir_image = np.asanyarray(ir_frame.get_data())
        ir_image = draw_overlay(ir_image, (0, 255, 0), f"{frame_count}")

        ret, buffer = cv2.imencode('.jpg', ir_image)

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
    port = int(sys.argv[1])
    print(f"Port Number {port}")

    # Start streaming
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.infrared)  # , 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    app.run(host='0.0.0.0', port=port, debug=False)  # Note: Setting debug to true causes the video capture to fail
