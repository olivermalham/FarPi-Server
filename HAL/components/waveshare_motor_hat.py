from HAL import HALComponent
from HAL.components.libs.waveshare_motor_hat.PCA9685 import PCA9685


class WaveshareMotorHat(HALComponent):
    """ Interface to the Waveshare motor hat for the Pi Zero. Supports two motors, connects via I2C using the
    PCA9685 library code from Waveshare.
    """

    def __init__(self, freq=50, i2c=0x40):
        """
        :param freq: PWM frequency, defaults to 50Hz
        :param i2c: I2C address of the controller, defaults to 0x40
        """
        super(HALComponent, self).__init__()
        self._pwm = PCA9685(i2c)
        self._pwm.setPWMFreq(freq)
        self._PWMA = 0
        self._AIN1 = 1
        self._AIN2 = 2
        self._PWMB = 5
        self._BIN1 = 3
        self._BIN2 = 4
        self.motor1_speed = 0
        self.motor2_speed = 0

    def refresh(self, hal):
        # Output only, nothing to refresh
        pass

    def action_run_motor1(self, value, hal):
        value = int(value)
        hal.message = f"Motor 1 speed set to {value}"
        self.motor1_speed = 100 if value > 100 else -100 if value < -100 else value

        if self.motor1_speed > 0:
            self._pwm.setLevel(self._AIN1, 0)
            self._pwm.setLevel(self._AIN2, 1)
        else:
            self._pwm.setLevel(self._AIN1, 1)
            self._pwm.setLevel(self._AIN2, 0)
        self._pwm.setDutycycle(self._PWMA, abs(self.motor1_speed))

    def action_run_motor2(self, value, hal):
        value = int(value)
        hal.message = f"Motor 2 speed set to {value}"
        self.motor2_speed = 100 if value > 100 else -100 if value < -100 else value

        if self.motor2_speed > 0:
            self._pwm.setLevel(self._BIN1, 0)
            self._pwm.setLevel(self._BIN2, 1)
        else:
            self._pwm.setLevel(self._BIN1, 1)
            self._pwm.setLevel(self._BIN2, 0)
        self._pwm.setDutycycle(self._PWMB, abs(self.motor2_speed))

    def action_stop_motor1(self, hal):
        hal.message = f"Stopping motor 1, speed was {self.motor1_speed}"
        self._pwm.setDutycycle(self._PWMA, 0)
        self.motor1_speed = 0

    def action_stop_motor2(self, hal):
        hal.message = f"Stopping motor 2, speed was {self.motor2_speed}"
        self._pwm.setDutycycle(self._PWMA, 0)
        self.motor2_speed = 0
