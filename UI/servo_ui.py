from themes.neon import *

"""
    Very simple panel which just shows one of each vanilla control.
"""

ui = Panel(
        Row(
                ToggleSwitch(pin="servo1", action="servo1.action_toggle", label="Servo Toggle"),
        ),
        Row(
                MessageBox()
        ),
        name="FarPi - Servo Test"
)
