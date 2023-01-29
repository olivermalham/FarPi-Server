"""
    HAL control that reads thermal imaging data from a XXX I2C sensor and converts it to an image
"""
from smbus import SMBus


class ThermalImager:

    def __init__(self, i2c_port, address=0x20):  # TODO: update address
        self.i2cbus = SMBus(i2c_port)  # Create a new I2C bus
        self.address = address

    def configure(self):
        self.i2cbus.write_byte_data(self.address, "IOCON", 0x02)  # TODO: This just a placeholder
        pass

    def next_frame(self):
        pass

