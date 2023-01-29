import argparse
import pyrealsense2.pyrealsense2 as realsense
import numpy as np
import cv2
from marvin_streams.marvin_feed import MarvinFeed
from marvin_streams.video_tools import VideoCrosshair, VideoText


class RealSenseVideoStream(VideoCrosshair, VideoText, MarvinFeed):

    def __init__(self, width=640, height=480, fps=30):
        super().__init__()
        self.width = width
        self.height = height
        self.fps = fps

        # Configure depth and color streams
        self.pipeline = realsense.pipeline()  # FIXME!
        self.config = realsense.config()

        # Get device product line for setting a supporting resolution
        self.pipeline_wrapper = realsense.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)

    def start(self):
        # Start streaming
        self.config.enable_stream(realsense.stream.depth, self.width, self.height, realsense.format.z16, self.fps)
        self.config.enable_stream(realsense.stream.color, self.width, self.height, realsense.format.bgr8, self.fps)
        self.config.enable_stream(realsense.stream.infrared)  # 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(self.config)

    @staticmethod
    def get_range(depth_frame, box):
        """ Return the average depth value of an area within the center of the depth frame """
        width = depth_frame.get_width()
        height = depth_frame.get_height()

        width_cen = int(width/2)
        height_cen = int(height/2)
        half_box = int(box/2)

        distance = 0.0  # Distance is in meters
        count = 0  # Number of valid range pixels

        for row in range(height_cen - half_box, height_cen + half_box):
            for column in range(width_cen - half_box, width_cen + half_box):
                new_distance = depth_frame.get_distance(column, row)
                distance = distance + new_distance
                count = count + 1 if new_distance > 0.0 else count
        distance = distance / count if count > 0 else 0.0
        return distance

    def next_depth_frame(self):
        frame_count = 0
        while True:
            frame_count = frame_count + 1
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            distance = self.get_range(depth_frame, 40)

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_color_mapped = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)

            depth_color_mapped = self.draw_text(depth_color_mapped, f"Frame No. {frame_count}", colour=(0, 0, 0))

            depth_color_mapped = self.draw_text(depth_color_mapped, f"{distance:.2f}m", font_scale=1.0,
                                                colour=(0, 0, 0),
                                                origin=(int(depth_frame.get_width()/2) + 25,
                                                        int(depth_frame.get_height()/2) + 15))

            depth_color_mapped = self.draw_crosshair(depth_color_mapped, (0, 0, 0), box=40)

            ret, buffer = cv2.imencode('.jpg', depth_color_mapped)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def next_colour_frame(self):
        frame_count = 0
        while True:
            frame_count = frame_count + 1
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            colour_frame = frames.get_color_frame()
            # Convert images to numpy arrays
            colour_image = np.asanyarray(colour_frame.get_data())
            colour_image = self.draw_text(colour_image, (0, 255, 0), f"Frame No. {frame_count}")
            colour_image = self.draw_crosshair(colour_image, (0, 255, 0))

            ret, buffer = cv2.imencode('.jpg', colour_image)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def next_ir_frame(self):
        frame_count = 0
        while True:
            frame_count = frame_count + 1
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            ir_frame = frames.get_infrared_frame()
            # Convert images to numpy arrays
            ir_image = np.asanyarray(ir_frame.get_data())
            ir_image = self.draw_text(ir_image, f"Frame No. {frame_count}", colour=(255, 255, 255))

            ret, buffer = cv2.imencode('.jpg', ir_image)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Realsense RGB Video Marvin feed")
    arg_parser.add_argument('--feed', dest='feed_name', action='store_const',
                            default='default_feed', help='Name of the feed to push data to')
    arg_parser.add_argument('--host', dest='host', action='store_const',
                            const=sum, default='127.0.0.1', help='Host name of Redis server')
    arg_parser.add_argument('--port', dest='port', action='store_const',
                            const=sum, default='6379', help='Name of the feed to push data to')

    arg_parser.parse_args()
    quit()
    with RealSenseVideoStream() as streamer:
        # print(f"Connection established, beginning stream to {redis_queue_name}")
        for data_frame in streamer.next_colour_frame():
            streamer.push_array(data_frame)
            #sleep(1)
        print("Stream terminated")
