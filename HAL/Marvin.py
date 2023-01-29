import HAL.components.gps
from .hal import *
from HAL.components.virtual import *
from HAL.components.MarvinMotion import MarvinMotion
from .base import BaseConsole, BaseGPIO


class MarvinHAL(HAL):
    """ HAL class for the Marvin rover project.

    """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(MarvinHAL, self).__init__()

        # We're using the BCM pin scheme
        # Add all the GPIO pins, setting pin and direction
        self.bcm00 = BaseGPIO(pin_number=0, directon=0)
        self.bcm01 = BaseGPIO(pin_number=1, directon=0)
        self.bcm02 = BaseGPIO(pin_number=2, directon=0)
        self.bcm03 = BaseGPIO(pin_number=3, directon=0)
        self.bcm04 = BaseGPIO(pin_number=4, directon=0)

        self.wave = GeneratorSquareWave()
        self.commandLine = BaseConsole()

        # self.motion = MarvinMotion()
        # self.gps = HAL.components.gps.GPS()

    def clean_up(self):
        super(MarvinHAL, self).clean_up()
