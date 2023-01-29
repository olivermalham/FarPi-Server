from .base import *
from HAL.components.servo import Servo, IndexedServo


class ServoHAL(BaseHAL):
    """ Slightly more specialised HAL that uses pigio for multichannel servo control.

    Note that the pigpio daemon needs to be running on the localhost, port 7777.
    All this does over the standard HAL is connect to the pigpio daemon.

    """
    def __init__(self):
        super(ServoHAL, self).__init__()

        self.servo1 = Servo(pin=3)
        self.servo2 = IndexedServo(pin=4, positions=[0.0, 0.25, 0.50, 0.75, 1.0])

    def clean_up(self):
        pass
