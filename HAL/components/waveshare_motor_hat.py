#!/usr/bin/python

from HAL.components.libs.waveshare_motor_hat.PCA9685 import PCA9685
import time

# TODO: This needs to be refactored and packed up as a FarPi component

Dir = [
    'forward',
    'backward',
]
pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50)


class MotorDriver:
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def run(self, motor, index, speed):
        if speed > 100:
            return
        if motor == 0:
            pwm.setDutycycle(self.PWMA, speed)
            if index == Dir[0]:
                print("1")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                print("2")
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if index == Dir[0]:
                print("3")
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                print("4")
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def stop(self, motor):
        if motor == 0:
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)


print("this is a motor driver test code")
Motor = MotorDriver()

print("forward 2 s")
Motor.run(0, 'forward', 10)
Motor.run(1, 'forward', 10)
time.sleep(2)

print("backward 2 s")
Motor.run(0, 'backward', 10)
Motor.run(1, 'backward', 10)
time.sleep(2)

print("stop")
Motor.stop(0)
Motor.stop(1)
