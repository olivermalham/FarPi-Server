from .hal import *
from .basic_pi import *
import pigpio

# TODO: Add a smooth-servo component that uses cubic hermite interpolation to smooth the movement. Ideally in a way
# TODO: that keeps all servos movements synchronised.


class Servo(HALComponent):
    """ Simple component for controlling a servo on any GPIO pin.

    Uses DMA to generate accurate PWM signals, via the pigpio library.
    """
    def __init__(self, pin=1, start=0.0, lower=1000, upper=2000, *args, **kwargs):
        super(Servo, self).__init__(*args, **kwargs)
        self._pin_number = pin
        # Group should be between 0 and 1.0
        self.state = start
        self._lower_bound = lower
        self._upper_bound = upper
        self._update = True

    def action_toggle(self, hal):
        """ Toggle the servo position between the two end points.

        :param hal:
        :return:
        """
        hal.message = "Servo action_toggle now:{}".format(self.state)

        self._update = True

        if self.state < 0.5:
            self.state = 1.0
        else:
            self.state = 0.0

    def action_set(self, value, hal):
        """ Move the servo to any arbitrary position between the two endpoints.

        :param value:
        :param hal:
        :return:
        """
        self._update = True

        self.state = value
        hal.message = "Servo action_set now:{}".format(self.state)

    def refresh(self, hal):
        if self._update:
            pulse = self.state * (self._upper_bound - self._lower_bound) + self._lower_bound
            hal.pi.set_servo_pulsewidth(self._pin_number, pulse)
            self._update = False


class IndexedServo(HALComponent):
    """ Simple component for controlling a servo on any GPIO pin.

    Uses DMA to generate accurate PWM signals, via the pigpio library.
    Indexed servo will only move the attached servo to one of N pre-defined positions.
    """
    def __init__(self, pin=1, lower=1000, upper=2000, start=0, positions=(0.0, 1.0), *args, **kwargs):
        super(IndexedServo, self).__init__(*args, **kwargs)
        self._pin_number = pin
        self._index = positions
        self.current_index = start
        self.max_index = len(positions) - 1

        # Group should be between 0 and 1.0
        self.state = positions[start]
        self._lower_bound = lower
        self._upper_bound = upper
        self._update = True
        self._hal = None

    def action_toggle_up(self, hal):
        """ Toggle the servo position between the two end points.

        :param hal:
        :return:
        """
        if self._hal is None:
            self._hal = hal

        hal.message = "IndexedServo action_toggle now:{}".format(self.state)
        self._update = True
        if self.current_index < self.max_index:
            self.current_index = self.current_index + 1

    def action_toggle_down(self, hal):
        """ Toggle the servo position between the two end points.

        :param hal:
        :return:
        """
        if self._hal is None:
            self._hal = hal

        hal.message = "IndexedServo action_toggle_up:{}".format(self.state)
        self._update = True
        if self.current_index > 0:
            self.current_index = self.current_index - 1

    def action_set(self, value, hal):
        """ Move the servo to any arbitrary position between the two endpoints.

        :param value:
        :param hal:
        :return:
        """
        if self._hal is None:
            self._hal = hal

        if value >= self.max_index:
            value = self.max_index
        if value < 0:
            value = 0

        self._update = True
        self.current_index = int(value)
        self.state = self._index[self.current_index]
        hal.message = "IndexedServo action_set now:{}".format(self.state)

    def refresh(self, hal):
        if self._update:
            self.state = self._index[self.current_index] * (self._upper_bound - self._lower_bound) + self._lower_bound
            hal.pi.set_servo_pulsewidth(self._pin_number, self.state)
            self._update = False


class ServoHAL(BasicPi):
    """ Slightly more specialised HAL that uses pigio for multi-channel servo control.

    Note that the pigpio daemon needs to be running on the localhost, port 7777.
    All this does over the standard HAL is connect to the pigpio daemon.

    """
    def __init__(self, *args, **kwargs):
        super(ServoHAL, self).__init__(*args, **kwargs)
        self.pi = pigpio.pi('localhost', 7777)

        self.servo1 = Servo(pin=3)
        self.servo2 = IndexedServo(pin=4, positions=[0.0, 0.25, 0.50, 0.75, 1.0])

    def clean_up(self):
        pass
