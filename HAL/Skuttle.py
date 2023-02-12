from .hal import *
from HAL.components.virtual import *
from .base import BaseConsole, BaseHAL
# from HAL.components.waveshare_motor_hat import WaveshareMotorHat


class SkuttleHAL(BaseHAL):
    """ HAL class for the Skuttle robot """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(SkuttleHAL, self).__init__()

        # We're using the BCM pin scheme

        self.wave = GeneratorSquareWave()
        self.commandLine = BaseConsole()

        # self.motors = WaveshareMotorHat()

    def clean_up(self):
        super(SkuttleHAL, self).clean_up()
