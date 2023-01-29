from HAL.components.virtual import *


class MockGPIO(HALComponent):
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


class MockRPIGPIO:

    OUT = 1
    IN = 0

    def __init__(self):
        pass

    @staticmethod
    def setup(pin_number=0, direction=1, pull_up_down=1):
        print(f"Mock RPi.GPIO setup pin: {pin_number}; direction: {direction}; pull: {pull_up_down}", flush=True)

    @staticmethod
    def output(pin_number=0, value=0):
        print(f"Mock RPi.GPIO setup pin: {pin_number}; value: {value}", flush=True)

    @staticmethod
    def input(pin_number=0):
        print(f"Mock RPi.GPIO input: {pin_number}", flush=True)
        return True

    @staticmethod
    def cleanup():
        print(f"Mock RPi.GPIO cleanup", flush=True)
