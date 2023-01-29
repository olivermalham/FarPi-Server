from .hal import HALComponent


"""
    Virtual components provide functionality above and beyond the basic GPIO type functions.

GroupToggle - Toggle a group of HALComponents between "on" and "off" states
GeneratorSawTooth - Generate a sawtooth waveform
TripWire - Sets an "on" state if a sensor passes a threshold, otherwise "off"
IfThisThen - Very powerful, generic If this, then that type component to create complex behaviours

"""


class Group(object):
    """ Simple container class that stores the kwargs as a dict.
    This is just so we get a slightly nicer syntax in the hal declaration

    """
    def __init__(self, *args, **kwargs):
        self.targets = kwargs


class GroupToggle(HALComponent):
    """ GroupToggle - Just toggles a group of controls between a preset "on" and "off" state

        Example usage:

        self.group1 = GroupToggle(on=Group(bcm00=1.0, bcm01=0.5, bcm03=0.0),
                                  off=Group(bcm00=0.0, bcm01=0.23, bcm03=1.0))
    """
    def __init__(self, on, off, *args, **kwargs):
        super(HALComponent, self).__init__()
        self.state = False
        self._on = on
        self._off = off

    def refresh(self, hal):
        pass

    def action_toggle(self, hal):
        self.state = not self.state
        hal.message = "GroupToggle action_toggle now:{}".format(self.state)
        if self.state:
            for target in self._on.targets:
                print("Setting {} = {}".format(target, self._on.targets[target]))
                component = getattr(hal, target)
                component.state = self._on.targets[target]
        else:
            for target in self._off.targets:
                print("Setting {} = {}".format(target, self._off.targets[target]))
                component = getattr(hal, target)
                component.state = self._off.targets[target]


class GeneratorSawTooth(HALComponent):
    """ Saw-tooth wave generator

    Produces an output that ramps from (low) to (high) with a step size of (delta)
    """

    def __init__(self, low=0.0, high=1.0, delta=0.1, *args, **kwargs):
        super(HALComponent, self).__init__()
        self.state = 0.0
        self.delta = delta
        self.low = low
        self.high = high

    def refresh(self, hal):
        self.state += self.delta
        if self.state >= self.high:
            self.state = self.low


class GeneratorSquareWave(HALComponent):
    """ Square wave generator

    Produces an output that ramps from (low) to (high) with a step size of (delta)
    """

    def __init__(self, period=10, *args, **kwargs):
        super(HALComponent, self).__init__()
        self.state = 0
        self.period = period / 2
        self.count = 0

    def refresh(self, hal):
        self.count = self.count + 1
        
        if self.count > self.period:
            self.state = not self.state
            self.count = 0


class TripWire(HALComponent):
    """ TripWire - Toggles a group of HALComponents to a preset "on" state if a sensor value passes a threshold,
    otherwise set an "off" state. Set falling=False to trip when the sensor is below the threshold.

        Example usage:

        self.tripwire = TripWire(sensor="bcm13", threshold=0.5,
                                 on=Group(bcm00=1.0, bcm01=0.5, bcm03=0.0),
                                 off=Group(bcm00=0.0, bcm01=0.23, bcm03=1.0))
    """
    def __init__(self, sensor, threshold, on, off, falling=False, *args, **kwargs):
        super(HALComponent, self).__init__()
        self.state = False
        self._on = on
        self._off = off
        self._sensor = sensor
        self._threshold = threshold
        self._falling = falling

    def refresh(self, hal):
        sensor_state = getattr(hal, self._sensor).state
        if not self._falling:
            self.state = (sensor_state > self._threshold)
        else:
            self.state = (sensor_state < self._threshold)

        if self.state:
            for target in self._on.targets:
                component = getattr(hal, target)
                component.state = self._on.targets[target]
        else:
            for target in self._off.targets:
                component = getattr(hal, target)
                component.state = self._off.targets[target]


class IfThisThen(HALComponent):
    """ If this, then that component

    Very powerful, and very generic. The "this" expression is assumed to be valid Python code, which is evaluated
    in the hals namespace. If the result is True, the "then" expression is executed. As with "this", "then" is also
    assumed to be valid Python code that is evaluated within the hals namespace. An option "else" expression will
    be evaluated if "this" evaluates to False. Note that the hal object itself is also added to the namespace, under
    the name "hal", so that it's methods may also be used.

    Example:
        self.iftt = IfThisThen(this="bcm01.state > 0.5 and bcm02.state <= 0.1",
                               then="bcm03.state=1.0",
                               otherwise="hal.message('IfThisThen otherwise statement')")
    """
    def __init__(self, this, then, otherwise=None):
        super(HALComponent, self).__init__()
        self._this = this
        self._then = then
        self._else = otherwise

    def refresh(self, hal):
        namespace = hal.__dict__
        namespace["hal"] = hal

        result = eval(self._this, namespace)
        if result:
            eval(self._then, namespace)
        elif self._else:
            eval(self._else, namespace)

