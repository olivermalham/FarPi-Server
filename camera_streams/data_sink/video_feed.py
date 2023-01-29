import cv2
from flask import Flask, Response
from ..marvin_array_feed import MarvinArrayFeed
import sys

# Initialize the Flask app
app = Flask(__name__)
port = 5000
feed_name = "video_rgb"


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
    page = f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <title>Marvin Video Stream</title>
                </head>
                <body>
                    <div class="container">
                        <div class="row">
                            <div class="col-lg-8  offset-lg-2">
                                Marvin video stream {feed_name}
                            </div>
                        </div>
                    </div>
                </body>
                </html>"""

    return page


@app.route(f'/{feed_name}')
def video_feed():
    # Use the co-routine to generate and send image frames
    return Response(fetch_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Marvin Image Feed Server")
        print("Usage:")
        print("     video_feed.py <stream name> <port number")
        quit(-1)

    feed_name = sys.argv[1]
    port = int(sys.argv[2])
    print(f"Marvin feed for stream {feed_name} ")
    print(f"Port Number {port}")

    with MarvinArrayFeed(stream=feed_name) as marvin_image_stream:
        app.run(host='0.0.0.0', port=port, debug=False)
