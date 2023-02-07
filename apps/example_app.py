# The Hardware Abstraction Layer (HAL) package represents the hardware attached to the server
# that the user will interact with via the UI
from apps.base_app import *
from UI import example_ui
from HAL.base import BaseHAL

# Number of milliseconds to delay between updates to clients
refresh_ms = 500

# Create the HAL object that interfaces with the hardware
hal = BaseHAL()
ui = example_ui.ui