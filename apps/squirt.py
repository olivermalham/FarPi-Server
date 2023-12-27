# The Hardware Abstraction Layer (HAL) package represents the hardware attached to the server
# that the user will interact with via the UI
from HAL.Squirt import SquirtHAL
from HAL.base import RemoteHAL

# Number of milliseconds to delay between updates to clients
refresh_ms = 50

# Create the HAL object that interfaces with the hardware
hal = [SquirtHAL(), RemoteHAL(port="/dev/ttyACM0", device_name="squirt_io")]
ui = "squirt"
http = False

# SSL files
cert = "./host.crt"
key = "./host.key"

# Name of the application, used when the launcher is scanning the network
name = "Squirt"
