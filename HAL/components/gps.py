import serial
import time
from HAL.hal import *
from HAL.components.libs.gps import GPSPacket


class GPS(HALComponent):
    """ Output only component that provides GPS data. """
    def __init__(self, port="/dev/ttyACM0", rate=115200, timeout=0.1):
        super(HALComponent, self).__init__()
        self._gps_port = port
        self._gps_serial = serial.Serial(self._gps_port, rate, timeout=timeout)

        self.time = time.time()
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.fix = False
        self.satellites = 0

    def refresh(self, hal):
        # If there is data waiting, read and parse the GPS packet, otherwise do nothing
        if not self._gps_serial.in_waiting:
            return

        data = self._gps_serial.readline()
        packet = GPSPacket.new(data)

        # Only process the packet if it is a standard position packet
        if packet is not None and packet.packet_type == "GPGGA":
            hal.message = f"GPS packet processed: {packet}"
            self.time = packet.time  # TODO: Build a real date-time object from the GPS time data
            self.latitude = packet.latitude
            self.longitude = packet.longitude
            self.altitude = packet.altitude
            self.fix = packet.gps_fix
            self.satellites = packet.number_satellites
