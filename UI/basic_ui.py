from themes.neon import *

ui = Panel(
        Row(
                PushButtonSwitch(pin="bcm00", label="bcm00"),
                PushButtonSwitch(pin="bcm01", label="bcm01"),
                PushButtonSwitch(pin="bcm02", label="bcm02"),
                PushButtonSwitch(pin="bcm03", label="bcm03"),
        ),
        Row(
                PushButtonSwitch(pin="bcm04", label="bcm04"),
                PushButtonSwitch(pin="bcm05", label="bcm05"),
                PushButtonSwitch(pin="bcm06", label="bcm06"),
                PushButtonSwitch(pin="bcm07", label="bcm07"),
        ),
        Row(
                PushButtonSwitch(pin="bcm08", label="bcm08"),
                PushButtonSwitch(pin="bcm09", label="bcm09"),
                PushButtonSwitch(pin="bcm10", label="bcm10"),
                PushButtonSwitch(pin="bcm11", label="bcm11"),
        ),
        Row(
                PushButtonSwitch(pin="bcm12", label="bcm12"),
                PushButtonSwitch(pin="bcm13", label="bcm13"),
                PushButtonSwitch(pin="bcm14", label="bcm14"),
                PushButtonSwitch(pin="bcm15", label="bcm15"),
        ),
        Row(
                PushButtonSwitch(pin="bcm16", label="bcm16"),
                PushButtonSwitch(pin="bcm17", label="bcm17"),
                PushButtonSwitch(pin="bcm18", label="bcm18"),
                PushButtonSwitch(pin="bcm19", label="bcm19"),
        ),
        Row(
                PushButtonSwitch(pin="bcm20", label="bcm20"),
                PushButtonSwitch(pin="bcm21", label="bcm21"),
                PushButtonSwitch(pin="bcm22", label="bcm22"),
                PushButtonSwitch(pin="bcm23", label="bcm23"),
        ),
        Row(
                PushButtonSwitch(pin="bcm24", label="bcm24"),
                PushButtonSwitch(pin="bcm25", label="bcm25"),
                PushButtonSwitch(pin="bcm26", label="bcm26"),
                PushButtonSwitch(pin="bcm27", label="bcm27"),
        ),

        Row(
                LED(pin="bcm00", label="LED"),
                PushButtonSwitch(pin="bcm01", label="Push button"),
                ToggleSwitch(pin="bcm02", action="bcm02.action_toggle", label="Toggle switch")
        ),
        Row(
                MessageBox()
        ),
        Row(
                LineGauge(source="dummy", label="Line Gauge")
        ),
)
