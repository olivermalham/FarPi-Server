from .themes.neon import *


"""
    Straightforward panel definition that just exposes all basic Raspberry Pi IO.

"""

ui = Panel(
        Row(
                ToggleSwitch(pin="bcm00", label="BCM00", action="bcm00.action_toggle"),
                ToggleSwitch(pin="bcm01", label="BCM01", action="bcm01.action_toggle"),
                ToggleSwitch(pin="bcm02", label="BCM02", action="bcm02.action_toggle"),
                ToggleSwitch(pin="bcm03", label="BCM03", action="bcm03.action_toggle"),
        ),
        Row(
                ToggleSwitch(pin="bcm04", label="BCM04", action="bcm04.action_toggle"),
                ToggleSwitch(pin="bcm05", label="BCM05", action="bcm05.action_toggle"),
                ToggleSwitch(pin="bcm06", label="BCM06", action="bcm06.action_toggle"),
                ToggleSwitch(pin="bcm07", label="BCM07", action="bcm07.action_toggle"),
        ),
        Row(
                ToggleSwitch(pin="bcm08", label="BCM08", action="bcm08.action_toggle"),
                ToggleSwitch(pin="bcm09", label="BCM09", action="bcm09.action_toggle"),
                ToggleSwitch(pin="bcm10", label="BCM10", action="bcm10.action_toggle"),
                ToggleSwitch(pin="bcm11", label="BCM11", action="bcm11.action_toggle"),
        ),
        Row(
                ToggleSwitch(pin="bcm12", label="BCM12", action="bcm12.action_toggle"),
                ToggleSwitch(pin="bcm13", label="BCM13", action="bcm13.action_toggle"),
                ToggleSwitch(pin="bcm14", label="BCM14", action="bcm14.action_toggle"),
                ToggleSwitch(pin="bcm15", label="BCM15", action="bcm15.action_toggle"),
        ),
        Row(
                ToggleSwitch(pin="bcm16", label="BCM16", action="bcm16.action_toggle"),
                ToggleSwitch(pin="bcm17", label="BCM17", action="bcm17.action_toggle"),
                ToggleSwitch(pin="bcm18", label="BCM18", action="bcm18.action_toggle"),
                ToggleSwitch(pin="bcm19", label="BCM19", action="bcm19.action_toggle"),
        ),
        Row(
                ToggleSwitch(pin="bcm20", label="BCM20", action="bcm20.action_toggle"),
                ToggleSwitch(pin="bcm21", label="BCM21", action="bcm21.action_toggle"),
                ToggleSwitch(pin="bcm22", label="BCM22", action="bcm22.action_toggle"),
                ToggleSwitch(pin="bcm23", label="BCM23", action="bcm23.action_toggle"),
        ),
        Row(
                ToggleSwitch(pin="bcm24", label="BCM24", action="bcm24.action_toggle"),
                ToggleSwitch(pin="bcm25", label="BCM25", action="bcm25.action_toggle"),
                ToggleSwitch(pin="bcm26", label="BCM26", action="bcm26.action_toggle"),
                ToggleSwitch(pin="bcm27", label="BCM27", action="bcm27.action_toggle"),
        ),
        Row(
                MessageBox()
        ),
        name="All the Pi",
)
