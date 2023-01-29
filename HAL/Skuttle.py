from collections import namedtuple
import serial
# from time import sleep
from .hal import *
from .virtual import *
from .basic_pi import BasicConsole
from skuttle.PCA9685 import PCA9685

LEGS = 0
TURN = 1


class SkuttleMotion(HALComponent):
    """ Component that communicates with the Marvin-core subsystem to handle low level movement 
    """
    def __init__(self):
        super(HALComponent, self).__init__()

        pwm = PCA9685(0x40, debug=True)
        pwm.setPWMFreq(50)

        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def refresh(self, hal):
        """ Use this to return the status of the current servo positions and motors
        """
        pass

    def action_move(self, hal, **kwargs):
        print(f"Received marvin motion command")
        hal.message = f"Marvin Motion - {kwargs}"

        speed = int(kwargs["speed"])
        heading = int(kwargs["heading"])

        self._update_motors(speed, 0)
    
    def action_turn(self, hal, **kwargs):
        print(f"Received marvin motion command")
        hal.message = f"Marvin Motion - {kwargs}"

        heading = int(kwargs["heading"])

        self._update_motors(0, heading)

    def action_stop(self, hal, **kwargs):
        print(f"Received marvin hard stop command")
        hal.message = f"Marvin hard stop!"
        self._setDutycycle(self.PWMA, 0)
        self._setDutycycle(self.PWMB, 0)
    
    def _update_motors(self, velocity, heading):
        """
        """

        # TODO: send to the controller via serial port
        pass


class SkuttleHAL(HAL):
    """ HAL class for the Skuttle robot

    """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(SkuttleHAL, self).__init__()

        # We're using the BCM pin scheme

        self.wave = GeneratorSquareWave()
        self.commandLine = BasicConsole()

        self.motion = SkuttleMotion()

    def clean_up(self):
        super(SkuttleHAL, self).clean_up()
