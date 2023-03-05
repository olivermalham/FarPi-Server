from .hal import *
from HAL.components.virtual import *


# If we can't import the RPI GPIO functionality, assume we're mocking
try:
    from RPi import GPIO
except ImportError:
    print("FAILED TO IMPORT RPi.GPIO, using MockRPIGPIO")
    from HAL.components.mock_pi import MockRPIGPIO as GPIO


class BaseGPIO(HALComponent):
    """ Basic GPIO pin """
    def __init__(self, pin_number=1, direction=GPIO.OUT, pull=None, *args, **kwargs):
        super(HALComponent, self).__init__()
        self.state = False
        self._pin_number = pin_number
        self._direction = direction
        if pull is not None:
            GPIO.setup(pin_number, direction, pull_up_down=pull)
        else:
            GPIO.setup(pin_number, direction)

    def refresh(self, hal):
        if self._direction == GPIO.IN:
            self.state = GPIO.input(self._pin_number)

    def action_toggle(self, hal):
        self.state = not self.state
        hal.message = "BasicPiGPIO action_toggle now:{}".format(self.state)
        GPIO.output(self._pin_number, self.state)

    def action_set(self, value, hal):
        hal.message = "BasicPiGPIO action_set value:{}".format(value)
        self.state = bool(value)
        GPIO.output(self._pin_number, self.state)


class BaseConsole(HALComponent):
    """ HAL component that processes commands sent from the client """

    def __init__(self):
        super(HALComponent, self).__init__()

    def refresh(self, hal):
        pass

    def action_command(self, command, hal):
        command_parts = command.split()
        print(f"Console command received: {command_parts[0]}")

        # Deliberately allow any exceptions thrown here to bubble up
        command_name = f"command_{command_parts[0]}"
        command = getattr(self, command_name)
        command(*command_parts[1:], hal=hal)

    def command_status(self, *args, hal):
        """ Example command method that is exposed to the client """
        print(f"Received console Status command")
        hal.message = f"{hal.prompt} Status is GREEN"


class BaseHAL(HAL):
    """ Concrete HAL class for accessing basic Raspberry Pi hardware.

    """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(BaseHAL, self).__init__()

        # We're using the BCM pin scheme
        GPIO.setmode(GPIO.BCM)

        # Add all the GPIO pins, setting pin and direction
        self.bcm00 = BaseGPIO(pin_number=0, directon=0)
        self.bcm01 = BaseGPIO(pin_number=1, directon=0)
        self.bcm02 = BaseGPIO(pin_number=2, directon=0)
        self.bcm03 = BaseGPIO(pin_number=3, directon=0)

        self.bcm04 = BaseGPIO(pin_number=4, directon=0)
        self.bcm05 = BaseGPIO(pin_number=5, directon=0)
        self.bcm06 = BaseGPIO(pin_number=6, directon=0)
        self.bcm07 = BaseGPIO(pin_number=7, directon=0)

        self.bcm08 = BaseGPIO(pin_number=8, directon=0)
        self.bcm09 = BaseGPIO(pin_number=9, directon=0)
        self.bcm10 = BaseGPIO(pin_number=10, directon=0)
        self.bcm11 = BaseGPIO(pin_number=11, directon=0)

        self.bcm12 = BaseGPIO(pin_number=12, directon=0)
        self.bcm13 = BaseGPIO(pin_number=13, directon=0)
        self.bcm14 = BaseGPIO(pin_number=14, directon=0)
        self.bcm15 = BaseGPIO(pin_number=15, directon=0)

        self.bcm16 = BaseGPIO(pin_number=16, directon=0)
        self.bcm17 = BaseGPIO(pin_number=17, directon=0)
        self.bcm18 = BaseGPIO(pin_number=18, directon=0)
        self.bcm19 = BaseGPIO(pin_number=19, directon=0)

        self.bcm20 = BaseGPIO(pin_number=20, directon=0)
        self.bcm21 = BaseGPIO(pin_number=21, directon=0)
        self.bcm22 = BaseGPIO(pin_number=22, directon=0)
        self.bcm23 = BaseGPIO(pin_number=23, directon=0)

        self.bcm24 = BaseGPIO(pin_number=24, directon=0)
        self.bcm25 = BaseGPIO(pin_number=25, directon=0)
        self.bcm26 = BaseGPIO(pin_number=26, directon=0)
        self.bcm27 = BaseGPIO(pin_number=27, directon=0)

        self.sawtooth = GeneratorSawTooth()
        self.square_wave = GeneratorSquareWave()

        self.commandLine = BaseConsole()

    def clean_up(self):
        super(BaseHAL, self).clean_up()
        GPIO.cleanup()
