# The Hardware Abstraction Layer (HAL) package represents the hardware attached to the server
# that the user will interact with via the UI
from HAL.Skuttle import SkuttleHAL

# Number of milliseconds to delay between updates to clients
refresh_ms = 500

# Create the HAL object that interfaces with the hardware
hal = SkuttleHAL()
ui = "skuttle"
http = True

# Name of the application, used when the launcher is scanning the network
name = "Skuttle"
