# Import the default settings from base_app
from apps.base_app import *
from UI import all_pi
# The Hardware Abstraction Layer (HAL) package represents the hardware attached to the server
# that the user will interact with via the UI
from HAL.mock import MockPi

# Number of milliseconds to delay between updates to clients
refresh_ms = 500

# Create the HAL object that interfaces with the hardware
hal = MockPi()

ui = all_pi.ui