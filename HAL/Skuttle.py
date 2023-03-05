from .hal import *
from HAL.components.virtual import *
from HAL.components.cpu import CPU
from .base import BaseHAL
from HAL.components.waveshare_motor_hat import WaveshareMotorHat
from HAL.components.control_console import ControlConsole


class SkuttleHAL(BaseHAL):
    """ HAL class for the Skuttle robot """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(SkuttleHAL, self).__init__()

        # We're using the BCM pin scheme

        self.wave = GeneratorSquareWave()
        self.commandLine = ControlConsole()

        self.motors = WaveshareMotorHat()

        self.cpu = CPU(temp="/sys/class/thermal/thermal_zone7/temp")

    def clean_up(self):
        super(SkuttleHAL, self).clean_up()
