from HAL.base import HAL, BaseConsole
from HAL.components.mock_pi import *


class MockPi(HAL):
    """ Mock HAL class for simulating basic Raspberry Pi hardware.

    """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(MockPi, self).__init__()

        # We're using the BCM pin scheme

        # Add all the GPIO pins, setting pin and direction
        self.bcm00 = MockGPIO(pin_number=0, directon=0)
        self.bcm01 = MockGPIO(pin_number=1, directon=0)
        self.bcm02 = MockGPIO(pin_number=2, directon=0)
        self.bcm03 = MockGPIO(pin_number=3, directon=0)

        self.bcm04 = MockGPIO(pin_number=4, directon=0)
        self.bcm05 = MockGPIO(pin_number=5, directon=0)
        self.bcm06 = MockGPIO(pin_number=6, directon=0)
        self.bcm07 = MockGPIO(pin_number=7, directon=0)

        self.bcm08 = MockGPIO(pin_number=8, directon=0)
        self.bcm09 = MockGPIO(pin_number=9, directon=0)
        self.bcm10 = MockGPIO(pin_number=10, directon=0)
        self.bcm11 = MockGPIO(pin_number=11, directon=0)

        self.bcm12 = MockGPIO(pin_number=12, directon=0)
        self.bcm13 = MockGPIO(pin_number=13, directon=0)
        self.bcm14 = MockGPIO(pin_number=14, directon=0)
        self.bcm15 = MockGPIO(pin_number=15, directon=0)

        self.bcm16 = MockGPIO(pin_number=16, directon=0)
        self.bcm17 = MockGPIO(pin_number=17, directon=0)
        self.bcm18 = MockGPIO(pin_number=18, directon=0)
        self.bcm19 = MockGPIO(pin_number=19, directon=0)

        self.bcm20 = MockGPIO(pin_number=20, directon=0)
        self.bcm21 = MockGPIO(pin_number=21, directon=0)
        self.bcm22 = MockGPIO(pin_number=22, directon=0)
        self.bcm23 = MockGPIO(pin_number=23, directon=0)

        self.bcm24 = MockGPIO(pin_number=24, directon=0)
        self.bcm25 = MockGPIO(pin_number=25, directon=0)
        self.bcm26 = MockGPIO(pin_number=26, directon=0)
        self.bcm27 = MockGPIO(pin_number=27, directon=0)

        self.sawtooth_wave = GeneratorSawTooth()
        self.square_wave = GeneratorSquareWave()

        self.commandLine = BaseConsole()

    def clean_up(self):
        super(MockPi, self).clean_up()
