# Import necessary libraries
from time import sleep
import numpy as np
import cv2
from ..marvin_array_feed import MarvinArrayFeed

# TODO: Generate a test frame, send to a redis queue. Consumer pulls the data and pushes it out as a JPG frame


def draw_overlay(frame, overlay_text):
    # Frames are ndarray objects, [y, x, blue, green, red]
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1.2
    color = (0, 255, 0)
    thickness = 1
    line_height = 15

    height = len(frame)

    lines = overlay_text.split("\n")
    orig = height - len(lines)*line_height
    for line in lines:
        frame = cv2.putText(frame, line, (10, orig), font, font_scale, color, thickness, cv2.LINE_AA)
        orig = orig + line_height
    return frame


def gen_image():
    frame_count = 0
    while True:
        # Convert images to numpy arrays
        image = np.zeros((500, 500, 3), np.uint8)
        image = draw_overlay(image, f"Test {frame_count}")
        frame_count = frame_count + 1
        yield image


redis_ip = "127.0.0.1"
redis_port = 6379
redis_queue_name = "image_feed"


if __name__ == "__main__":
    print("Redis Image Streamer")
    print(f"Connecting to server {redis_ip}:{redis_port}...")
    frame_no = 0

    with MarvinArrayFeed(stream="image_feed") as marvin_client:
        print(f"Connection established, beginning stream to {redis_queue_name}")
        for data_frame in gen_image():
            marvin_client.push_array(data_frame)
            sleep(1)
    print("Stream terminated")

