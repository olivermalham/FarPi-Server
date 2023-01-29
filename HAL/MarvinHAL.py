from collections import namedtuple
import serial
# from time import sleep
from .hal import *
from .virtual import *
from .servo_lib.lewansoul_lx16a import ServoController
from .basic_pi import BasicConsole

# UART serial port for servo bus
SERVO_SERIAL_PORT = '/dev/serial0'

# Constants that define servo bus ids for each function
WHEEL_1 = 1
WHEEL_2 = 2
WHEEL_5 = 3
WHEEL_6 = 4
HEAD_YAW = 5
HEAD_PITCH = 6

ServoCalib = namedtuple("ServoCalib", "scale origin limit_low limit_high")


class MarvinGPIO(HALComponent):
    """ Basic GPIO pin.

    """
    def __init__(self, pin_number=1, direction=True, pull=None, *args, **kwargs):
        super(HALComponent, self).__init__()
        self.state = False
        self._pin_number = pin_number
        self._direction = direction

    def refresh(self, hal):
        # self.state = not self.state
        # if self._direction:
        #    self.state = state
        pass

    def action_toggle(self, hal):
        self.state = not self.state
        hal.message = f"Pin {self._pin_number} toggled; now:{self.state}"

    def action_set(self, value, hal):
        hal.message = "BasicPiGPIO action_set value:{}".format(value)
        self.state = bool(value)


class MarvinMotion(HALComponent):
    """ Component that communicates with the Marvin-core subsystem to handle low level movement 
    """
    def __init__(self):
        super(HALComponent, self).__init__()

        # self._motion_fifo = open("/etc/marvin/motion", "w")
        # self._motion_fifo = open("/etc/marvin/motion_test", "w")

        self._motion_packet = { "move": {"distance": 0, "speed": 0.0},
                                "turn": {"angle": 0, "speed": 0.0},
                                "head": {"pitch": 0, "yaw": 0},
                                "action": None
                                }

        # Servo calibration settings for converting from degrees to servo units
        # Note that entry 0 is None as we're mapping servo id's here, which start at 1
        # Limits are in degrees, not servo units. Origin is the offset corresponding to
        # zero degrees. Making the scale value negative should reverse the movement
        self.servo_calib = [None,
                            ServoCalib(scale=5.952, origin=500, limit_low=-84.0, limit_high=84.0),
                            ServoCalib(scale=5.952, origin=500, limit_low=-84.0, limit_high=84.0),
                            ServoCalib(scale=5.952, origin=500, limit_low=-84.0, limit_high=84.0),
                            ServoCalib(scale=5.952, origin=500, limit_low=-84.0, limit_high=84.0),
                            ServoCalib(scale=3.7, origin=500, limit_low=-135.0, limit_high=135.0),  # Yaw
                            ServoCalib(scale=3.7, origin=500, limit_low=-41.0, limit_high=41.0)]  # Pitch

        self._servo_controller = ServoController(
            serial.Serial(SERVO_SERIAL_PORT, 115200, timeout=0.2),
            timeout=0.5
        )

        self.head_pitch = self._to_degrees(HEAD_PITCH, self._servo_controller.get_position(HEAD_PITCH))
        self.head_yaw = self._to_degrees(HEAD_YAW, self._servo_controller.get_position(HEAD_YAW))
        self.wheel1_angle = self._servo_controller.get_position(WHEEL_1)
        self.wheel2_angle = self._servo_controller.get_position(WHEEL_2)
        self.wheel5_angle = self._servo_controller.get_position(WHEEL_5)
        self.wheel6_angle = self._servo_controller.get_position(WHEEL_6)

    def refresh(self, hal):
        """ Use this to return the status of the current servo positions and motors
        """
        self.head_pitch = self._to_degrees(HEAD_PITCH, self._servo_controller.get_position(HEAD_PITCH))
        self.head_yaw = self._to_degrees(HEAD_YAW, self._servo_controller.get_position(HEAD_YAW))

    def action_move(self, hal, **kwargs):
        print(f"Received marvin motion command")
        hal.message = f"Marvin Motion - {kwargs}"

        vel = int(kwargs["speed"])
        dist = int(kwargs["distance"])

        command = f"MOVE:"
        command = command + f"M1,D{dist},V{vel};"
        command = command + f"M2,D{dist},V{vel};"
        command = command + f"M3,D{dist},V{vel};"
        command = command + f"M4,D{dist},V{vel};"
        command = command + f"M5,D{dist},V{vel};"
        command = command + f"M6,D{dist},V{vel};"

        self._update_motors(command)
    
    def action_turn(self, hal, **kwargs):
        print(f"Received marvin motion command")
        hal.message = f"Marvin Motion - {kwargs}"

        angle = int(kwargs["angle"])
        speed = int(kwargs["speed"])
        d_outer = 0  # TODO: Calc!
        v_outer = 255
        d_inner = 0  # TODO: Calc!
        v_inner = 128  # TODO: Calc!

        command = f"MOVE:"
        command = command + f"M1,D{d_outer},V{v_outer};"
        command = command + f"M2,D{d_outer},V{v_outer};"
        command = command + f"M3,D{d_inner},V{v_inner};"
        command = command + f"M4,D{d_inner},V{v_inner};"
        command = command + f"M5,D{d_outer},V{v_outer};"
        command = command + f"M6,D{d_outer},V{v_outer};"

        self._update_motors(command)

    def action_head_yaw(self, hal, **kwargs):
        print(f"Received marvin head yaw command")
        if "delta" in kwargs:
            angle = self.head_yaw + int(kwargs["delta"])
            time = 100
        else:
            angle = int(kwargs["angle"])
            time = 500

        hal.message = f"Marvin Head Yaw {angle} degrees"
        self._servo_controller.move(HEAD_YAW, self._to_servo(HEAD_YAW, angle), time)
        self.head_yaw = self._to_degrees(HEAD_YAW, self._servo_controller.get_position(HEAD_YAW))

    def action_head_pitch(self, hal, **kwargs):
        print(f"Received marvin head pitch command")
        if "delta" in kwargs:
            angle = self.head_pitch + int(kwargs["delta"])
            time = 100
        else:
            angle = int(kwargs["angle"])
            time = 500

        hal.message = f"Marvin Head Pitch {angle} degrees"
        self._servo_controller.move(HEAD_PITCH, self._to_servo(HEAD_PITCH, angle), time)
        self.head_pitch = self._to_degrees(HEAD_PITCH, self._servo_controller.get_position(HEAD_PITCH))

    def action_stop(self, hal, **kwargs):
        print(f"Received marvin hard stop command")
        hal.message = f"Marvin hard stop!"
        self._update_motors("HARDSTOP;")
    
    def action_head_center(self, hal):
        print(f"Received marvin head motion command")
        hal.message = f"Marvin Head Center"
        self._servo_controller.move(HEAD_PITCH, self.servo_calib[HEAD_PITCH].origin, 1000)
        self._servo_controller.move(HEAD_YAW, self.servo_calib[HEAD_YAW].origin, 1000)
        self.head_yaw = 0
        self.head_pitch = 0

    def _update_motors(self, command):
        """ Send motor control commands to the controller on the serial port

            MOVE Command
            Format:
            MOVE:D<motor 1 distance>,V<motor 1 velocity>....D<motor 6 distance>,V<motor 6 velocity>;
            e.g.
            MOVE:D0.0,V0.0,D1.0,V1.0,D2.0,V2.0,D3.0,V3.0,D4.0,V4.0,D5.0,V5.0
        """

        # TODO: send to the controller via serial port
        print(command)

    def _to_servo(self, servo_no, angle):
        """ Convert the given servo position in degrees into servo units. """
        angle = self.servo_calib[servo_no].limit_low if angle < self.servo_calib[servo_no].limit_low else angle
        angle = self.servo_calib[servo_no].limit_high if angle > self.servo_calib[servo_no].limit_high else angle
        servo_pos = self.servo_calib[servo_no].origin + (self.servo_calib[servo_no].scale * angle)
        print(f"_to_servo({servo_no}, {angle}) = {servo_pos}")
        return servo_pos

    def _to_degrees(self, servo_no, position):
        """ Convert the given servo position in degrees into servo units. """
        angle = (position - self.servo_calib[servo_no].origin) / self.servo_calib[servo_no].scale
        return angle


class MarvinHAL(HAL):
    """ Mock HAL class for simulating basic Raspberry Pi hardware.

    """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(MarvinHAL, self).__init__()

        # We're using the BCM pin number scheme

        # Add all the GPIO pins, setting pin number and direction
        self.bcm00 = MarvinGPIO(pin_number=0, directon=0)
        self.bcm01 = MarvinGPIO(pin_number=1, directon=0)
        self.bcm02 = MarvinGPIO(pin_number=2, directon=0)
        self.bcm03 = MarvinGPIO(pin_number=3, directon=0)
        self.bcm04 = MarvinGPIO(pin_number=4, directon=0)

        self.wave = GeneratorSquareWave()
        self.commandLine = BasicConsole()

        self.motion = MarvinMotion()

    def clean_up(self):
        super(MarvinHAL, self).clean_up()
