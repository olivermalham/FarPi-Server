from .hal import *
from HAL.components.cpu import CPU
from .base import BaseHAL, BaseGPIO
from HAL.components.control_console import ControlConsole


class SquirtHAL(BaseHAL):
    """ HAL class for the Skuttle robot """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(SquirtHAL, self).__init__()

        # We're using the BCM pin scheme
        self.commandLine = ControlConsole()

        # Thermal zone 0 for the R.Pi
        self.cpu = CPU(temp="/sys/class/thermal/thermal_zone0/temp")

        # Most IO handled by Pico communicating via JSON over USB serial console
        # TODO: Need to write some kind of pass-through component

    def clean_up(self):
        super(SquirtHAL, self).clean_up()
