import websocket

# Utility to log the datastream and video feed(s) from a FarPi server
#
# Requires ffmpeg for handling the video feed, this utility just handles the file management and running the process
#
# ffmpeg -f mjpeg -i "http://192.168.0.245:8080/stream" ./video.avi

# Create a date stamped directory within the logging folder
# Create a json file to write the data stream from the websocket to
# Monitor the data stream. When the "logging" variable is set, start logging
# Four logging options - "none", "data", "video", "all"
# For "all" and "video" use ffmpeg to record the video feed. TODO: Figure out what format is best to use


URL = "ws://127.0.0.1:8888/farpi"


def on_message(ws, message):
    print(f"Message: {message}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("Opened connection")


ws = websocket.WebSocketApp(URL,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever(reconnect=5)
