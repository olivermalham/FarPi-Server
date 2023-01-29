import numpy as np
import cv2

"""
    Mixin classes for drawing features on video feeds
"""


class VideoText:

    @staticmethod
    def draw_text(frame, overlay_text, origin=None,
                  colour=(0, 255, 0), font_scale=1.2, thickness=1, line_height=15,
                  font=cv2.FONT_HERSHEY_PLAIN):
        """
        Draw text in the lower left corner of the video frame. Parameters are self-explanatory.

        :param frame: ndarray object [y, x, blue, green, red]
        :param overlay_text:
        :param origin: (x, y) tuple, specifies lower-left point. If None, text drawn in bottom left corner
        :param colour:
        :param font_scale:
        :param thickness:
        :param line_height:
        :param font:
        :return:
        """
        height = len(frame)

        lines = overlay_text.split("\n")
        if origin is None:
            origin = (10, height - len(lines)*line_height)

        for line in lines:
            frame = cv2.putText(frame, line, origin, font, font_scale, colour, thickness, cv2.LINE_AA)
            origin = (origin[0], origin[1] + line_height)
        return frame


class VideoCrosshair:

    @staticmethod
    def draw_crosshair(frame, colour=(0, 255, 0), minor_tick=5, major_tick=10, line_width=1, box=0):
        """
        Draw a crosshair overlay on the video frame.

        :param frame: ndarray object, [y, x, blue, green, red]
        :param colour:
        :param minor_tick:
        :param major_tick:
        :param line_width:
        :param box:
        :return:
        """

        width = len(frame)
        height = len(frame[0])

        width_cen = int(width/2)
        height_cen = int(height/2)
        half_box = int(box/2)

        # Main crosshair lines
        cv2.line(frame, (height_cen, 0), (height_cen, width_cen - half_box), colour, line_width)
        cv2.line(frame, (height_cen, width_cen + half_box), (height_cen, width), colour, line_width)

        cv2.line(frame, (0, width_cen), (height_cen - half_box, width_cen), colour, line_width)
        cv2.line(frame, (height_cen + half_box, width_cen), (height, width_cen), colour, line_width)

        if box > 0:
            # Central box
            cv2.rectangle(frame, (height_cen - half_box, width_cen - half_box),
                          (height_cen + half_box, width_cen + half_box), colour, line_width)

        if minor_tick > 0:
            # Minor ticks
            for i in range(20, height, 40):
                cv2.line(frame, (i, width_cen-minor_tick), (i, width_cen+minor_tick), colour, line_width)
            for i in range(20, width, 40):
                cv2.line(frame, (height_cen-minor_tick, i), (height_cen+minor_tick, i), colour, line_width)

        if major_tick > 0:
            # Major ticks
            for i in range(40, height, 40):
                cv2.line(frame, (i, width_cen-major_tick), (i, width_cen+major_tick), colour, line_width)
            for i in range(40, width, 40):
                cv2.line(frame, (height_cen-major_tick, i), (height_cen+major_tick, i), colour, line_width)

        return frame
