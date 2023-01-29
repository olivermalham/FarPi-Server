import json


class HAL(object):
    """ Hardware Abstraction Layer

        Provides a framework for HAL components to interact with the state vector.
        Rather than implement the state vector as a nested dictionary of named values,
        HAL uses object introspection to work with itself directly.
        HALComponent subclasses are added to a HAL subclass as class attributes.
        Should be a singleton class, created in the settings file.
        Coercing this class into a string serialises into JSON.

        Idea:

        RaspBerryPi(HAL):
            gpio01 = RPIO_GPIOpin(1)
            gpio02 = RPIO_GPIOpin(2)
            gpio03 = RPIO_GPIOpin(3)
            gpio04 = RPIO_GPIOpin(4)
            gpio05 = RPIO_GPIOpin(5)
            temp = I2CThermistor(bus address)
    """

    def __init__(self, *args, **kwargs):
        # Simple counter that gets incremented on every refresh
        self.cycle = 0

        # Message to the client. Up to the client to store them if required
        self.message = "FarPi - HAL Initialised"

        self.error = ""

    def clean_up(self):
        """ Make sure any resources the HAL uses get released.

        :return:
        """
        pass

    def action(self, name, **kwargs):
        """ Dispatch an action received via the WebSockets server

        Name is treated as a valid python attribute reference. It is assumed that
        the FarPi server has already checked the string for security.
        :param name: String containing the name of the action to invoke
        :param kwargs: One or more key word arguments, decoded from JSON
        :return: Nothing
        """
        target = eval(name, self.__dict__)
        if callable(target):
            # Pass the HAL instance down to the component
            kwargs["hal"] = self
            target(**kwargs)

    def serialise(self):
        """ Encode the state vector as a JSON object

        :return: String containing the JSON encoded state vector
        """
        result = "{"
        for entry_name in dir(self):
            entry = getattr(self, entry_name)
            if not callable(entry) and not entry_name.startswith("_"):
                if issubclass(entry.__class__, HALComponent):
                    result = result + '"{}":{},'.format(entry_name, entry.serialise(entry_name))
                else:
                    result = result + '"{}":"{}",'.format(entry_name, str(entry))
        result = result[:-1] + "}"

        # Clear the message text now that its been serialised and sent to the client.
        self.message = ""
        self.error = ""

        return result

    def refresh(self):
        """ Refresh the state vector to the current hardware state.

            Run through all active HALComponents and call their refresh methods
        :return: Nothing
        """
        self.cycle += 1

        for entry in dir(self):
            if not entry.startswith("_"):
                component = getattr(self, entry)
                if issubclass(component.__class__, HALComponent):
                    component.refresh(self)


class HALComponent(object):
    """ Abstract base class that represents a single hardware component.

    """

    def __init__(self, *args, **kwargs):
        pass

    def serialise(self, instance_name):
        result = {}
        actions = []
        for entry in dir(self):
            if not entry.startswith("_"):
                attribute = getattr(self, entry)
                if not callable(attribute):
                    result[entry] = attribute
                elif entry.startswith("action_"):
                    actions.append("{}.{}".format(instance_name, entry))
        result["actions"] = actions
        return json.dumps(result)

    def refresh(self, hal):
        """ Interrogate the underlying hardware and update our state to match.

        :return: Nothing
        """
        raise NotImplementedError
