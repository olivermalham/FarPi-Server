from .hal import *
from HAL.components.virtual import *
import serial


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


class BaseFlag(HALComponent):
    """ Very simple binary flag, has no direct impact on hardware.
    Used for passing state between FarPi clients"""

    def __init__(self):
        super(HALComponent, self).__init__()
        self.state = False

    def refresh(self, hal):
        pass

    def action_toggle(self, hal):
        self.state = not self.state

    def action_enable(self, hal):
        self.state = True

    def action_disable(self, hal):
        self.state = False


class BaseHAL(HAL):
    """ Concrete HAL class for accessing basic Raspberry Pi hardware.

    """

    def __init__(self):
        # Make sure the HAL system is initialised fully first
        super(BaseHAL, self).__init__()

        # We're using the BCM pin scheme
        GPIO.setmode(GPIO.BCM)

        # Add all the GPIO pins, setting pin and direction
        self.bcm00 = None
        self.bcm01 = None
        self.bcm02 = None
        self.bcm03 = None

        self.bcm04 = None
        self.bcm05 = None
        self.bcm06 = None
        self.bcm07 = None

        self.bcm08 = None
        self.bcm09 = None
        self.bcm10 = None
        self.bcm11 = None

        self.bcm12 = None
        self.bcm13 = None
        self.bcm14 = None
        self.bcm15 = None

        self.bcm16 = None
        self.bcm17 = None
        self.bcm18 = None
        self.bcm19 = None

        self.bcm20 = None
        self.bcm21 = None
        self.bcm22 = None
        self.bcm23 = None

        self.bcm24 = None
        self.bcm25 = None
        self.bcm26 = None
        self.bcm27 = None

        self.sawtooth = GeneratorSawTooth()
        self.square_wave = GeneratorSquareWave()

        self.commandLine = BaseConsole()

        self.logging = BaseFlag()

    def config_basic_pins(self):
        """
            Configure all the basic Raspberry Pi pins as outputs. Pulled out from init to give subclasses the
            choice if they want to use this. Avoids potential conflicts with other components.
        """
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

    def clean_up(self):
        super(BaseHAL, self).clean_up()
        GPIO.cleanup()


class RemoteHAL(HAL):
    """ Connects to a HAL running on a microcontroller via serial link.
    Passes all actions through, fetches state updates.
    """

    def __init__(self, port, device_name):
        # Make sure the HAL system is initialised fully first
        super(RemoteHAL, self).__init__()
        self._data = "{}"
        self._buffer = ""
        self._path = port
        self._device = device_name

        try:
            # Non-blocking
            self._com_port = serial.Serial(port, 115200, timeout=0)
            print(f"RemoteHAL {self._device} Started on {self._path}")
        except serial.serialutil.SerialException:
            print(f"FAILED TO OPEN SERIAL PORT {port}")
            self._com_port = None

    def action(self, name, **kwargs):
        """ Dispatch an action received via the WebSockets server
        Rebuild the action string and pass it through to the attached microcontroller

        :param name: String containing the name of the action to invoke
        :param kwargs: One or more key word arguments, decoded from JSON
        :return: Nothing
        """

        # Remote device does not handle component names, so filter them out
        if not self._device.startswith(name):
            return

        # Build arguments back into a JSON action string and send through to the Pico
        args = ""
        for param, value in kwargs:
            args = args + '"' + param + '":"' + value + '",'
        action_string = '{"action":"' + name + '", "parameters":{' + args[:-1] + '}}\n'
        if self._com_port:
            self._com_port.write(action_string)
        else:
            print(f"RemoteHAL: {action_string}")

    def serialise(self):
        """ Just return the latest JSON packet fetched from the microcontroller

        :return: String containing the JSON encoded state vector
        """

        # Clear the message text now that it's been serialised and sent to the client.
        self.message = ""
        self.error = ""
        # Wrap the state data from the device into JSON structure that
        return '{"' + self._device + '":' + self._data + '}'

    def refresh(self):
        """ Read the latest state data from the serial link and store it.

        :return: Nothing
        """
        if self._com_port:
            new_data = self._com_port.read(20)  # None blocking read, accumulate into buffer
            self._buffer += new_data.decode(encoding='utf-8', errors='strict')

        # Data should always be a one-line JSON string
        if "\n" in self._buffer:
            parts = self._buffer.split("\r\n")
            self._data = parts[0] if self._valid_json(parts[0]) else self._data
            self._buffer = parts[1]
            print(f"RemoteHAL data: {self._data}", flush=True)
        self.cycle += 1

    @staticmethod
    def _valid_json(json_data):
        try:
            json.loads(json_data)
        except ValueError as err:
            return False
        return True
