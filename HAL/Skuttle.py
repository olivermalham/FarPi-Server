from .hal import *
from HAL.components.virtual import *
from HAL.components.cpu import CPU
from .base import BaseHAL, BaseGPIO
from HAL.components.waveshare_motor_hat import WaveshareMotorHat
from HAL.components.control_console import ControlConsole
from HAL.components.displayhatmini import DisplayHATMini


class SkuttleHAL(BaseHAL):
    """ HAL class for the Skuttle robot """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(SkuttleHAL, self).__init__()

        # We're using the BCM pin scheme

        self.wave = GeneratorSquareWave()
        self.commandLine = ControlConsole()

        self.motors = WaveshareMotorHat()

        # Thermal zone 0 for the R.Pi
        self.cpu = CPU(temp="/sys/class/thermal/thermal_zone0/temp")

        self.display = DisplayHATMini()

        # Configure the pins for the display hat mini
        self.led_r = BaseGPIO(pin_number=17, directon=0)
        self.led_g = BaseGPIO(pin_number=27, directon=0)
        self.led_b = BaseGPIO(pin_number=22, directon=0)

        self.switch_a = BaseGPIO(pin_number=5, directon=1)
        self.switch_b = BaseGPIO(pin_number=6, directon=1)
        self.switch_x = BaseGPIO(pin_number=16, directon=1)
        self.switch_y = BaseGPIO(pin_number=24, directon=1)

    def clean_up(self):
        super(SkuttleHAL, self).clean_up()
