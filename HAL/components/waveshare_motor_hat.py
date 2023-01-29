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
        self.pwm = PCA9685(i2c)
        self.pwm.setPWMFreq(freq)
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4
        self.motor1_speed = 0
        self.motor2_speed = 0

    def refresh(self, hal):
        # Output only, nothing to refresh
        pass

    def action_run_motor1(self, speed, hal):
        hal.message = f"Motor 1 speed set to {speed}"
        self.motor1_speed = 100 if speed > 100 else -100 if speed < -100 else speed

        self.pwm.setDutycycle(self.PWMA, self.motor1_speed)
        if self.motor1_speed > 0:
            self.pwm.setLevel(self.AIN1, 0)
            self.pwm.setLevel(self.AIN2, 1)
        else:
            self.pwm.setLevel(self.AIN1, 1)
            self.pwm.setLevel(self.AIN2, 0)

    def action_run_motor2(self, speed, hal):
        hal.message = f"Motor 2 speed set to {speed}"
        self.motor2_speed = 100 if speed > 100 else -100 if speed < -100 else speed

        self.pwm.setDutycycle(self.PWMB, self.motor2_speed)
        if self.motor2_speed > 0:
            self.pwm.setLevel(self.BIN1, 0)
            self.pwm.setLevel(self.BIN2, 1)
        else:
            self.pwm.setLevel(self.BIN1, 1)
            self.pwm.setLevel(self.BIN2, 0)

    def action_stop_motor1(self, hal):
        hal.message = f"Stopping motor 1, speed was {self.motor1_speed}"
        self.pwm.setDutycycle(self.PWMA, 0)
        self.motor1_speed = 0

    def action_stop_motor2(self, hal):
        hal.message = f"Stopping motor 2, speed was {self.motor2_speed}"
        self.pwm.setDutycycle(self.PWMA, 0)
        self.motor2_speed = 0
