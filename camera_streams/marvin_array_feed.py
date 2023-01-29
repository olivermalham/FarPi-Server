import struct
import numpy as np
from marvin_feed import MarvinFeed


class MarvinArrayFeed(MarvinFeed):
    """
        Feeds numpy arrays to or from a Redis stream
    """

    def __init__(self, host="127.0.0.1", port=6379, stream="default_image_stream",
                 group="default_group", consumer_name="unique ID here"):
        super().__init__(host="127.0.0.1", port=6379, stream="default_image_stream",
                         group="default_group", consumer_name="unique ID here")

    def push_array(self, data):
        """ Store given Numpy array data in Redis queue. Note that the dimensions of the
        array are stored as a packed binary struct immediately before the data
        """
        height, width, depth = data.shape
        shape = struct.pack('>III', height, width, depth)
        encoded = shape + data.tobytes()

        # Store encoded data in Redis
        self.push(encoded)
        return

    def next_array(self):
        """ Retrieve Numpy array from Redis queue. The dimensions of the array are stored as a
        packed binary struct that must be removed from the raw data before building the np array
        """
        encoded = self.next()[b'data']
        if encoded is None:
            raise Exception  # TODO: Need a better exception!
        height, width, depth = struct.unpack('>III', encoded[:12])
        # Slicing here to remove the packed struct
        data = np.frombuffer(encoded[12:], dtype=np.uint8).reshape(height, width, depth)  # TODO: Datatype!
        return data
