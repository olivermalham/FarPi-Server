"""
    HAL control that reads thermal imaging data from a XXX I2C sensor and converts it to an image
"""
from smbus import SMBus


# TODO: Package as a component
# TODO: Write the code!
class ThermalImager:

    def __init__(self, i2c_port, address=0x20):  # Is this address correct?
        self.i2cbus = SMBus(i2c_port)  # Create a new I2C bus
        self.address = address

    def configure(self):
        self.i2cbus.write_byte_data(self.address, "IOCON", 0x02)  # This just a placeholder
        pass

    def next_frame(self):
        pass

