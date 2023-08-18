# The Hardware Abstraction Layer (HAL) package represents the hardware attached to the server
# that the user will interact with via the UI
from HAL.base import BaseHAL

# Number of milliseconds to delay between updates to clients
refresh_ms = 500

# Create the HAL object that interfaces with the hardware
hal = BaseHAL()
ui = "demo"

# Name of the application, used when the launcher is scanning the network
name = "Demo"
