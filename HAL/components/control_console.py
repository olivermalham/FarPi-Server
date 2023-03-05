import time
from HAL.hal import *


class ControlConsole(HALComponent):
    """
        Extended console component that can store and execute lists of HAL actions sent from the client
    """

    def __init__(self):
        super(HALComponent, self).__init__()
        self.command_buffer = []
        self.program_mode = False

    def refresh(self, hal):
        pass

    def action_command(self, command, hal):
        command_parts = command.split()
        print(f"Console command received: {command_parts[0]}")

        # Deliberately allow any exceptions thrown here to bubble up
        command_name = f"command_{command_parts[0]}"
        if hasattr(self, command_name):
            command = getattr(self, command_name)
            command(*command_parts[1:], hal=hal)
            if self.program_mode:
                self.command_buffer.append(command_parts)
        else:
            self.execute_action(hal, command_parts)

    def execute_action(self, hal, command_parts):
        action = f"{command_parts[0]}.action_{command_parts[1]}"
        args = {}
        for part in command_parts[2:]:
            if "=" in part:
                bits = part.split("=")
                args[bits[0]] = bits[1]
            else:
                args["value"] = part
        hal.action(action, **args)

    def command_clear(self, *args, hal):
        """ Clear the instruction buff """
        self.command_buffer = []
        hal.message = "Program cleared"

    def command_list(self, *args, hal):
        """ Return the list of all commands in the buffer """
        hal.message = "1. wibble \\n2. wobble\\n3. blah\\n"

    def command_program(self, *args, hal):
        """ Start programming mode """
        self.program_mode = True
        hal.message = "Start program"

    def command_end(self, *args, hal):
        """ Exit programming mode """
        self.program_mode = False
        hal.message = "End program"

    def command_help(self, *args, hal):
        """ Send help info back """
        target = hal
        if len(args) and args[0] != "_" and isinstance(getattr(hal, args[0]), HALComponent):
            hal.message = f"{args[0]} actions:"
            target = getattr(hal, args[0])
            self.help_component(hal, target)
        else:
            self.help_console(hal)
            self.help_hal(hal)

    def help_console(self, hal):
        hal.message += "\\nConsole commands:"
        for item in dir(self):
            if item.startswith("command_") and callable(getattr(self, item)):
                hal.message = hal.message + "\\n\\t" + item.replace("command_", "")

    def help_hal(self, hal):
        hal.message += "\\nAvailable components:"
        for item in dir(hal):
            if item[0] != "_" and isinstance(getattr(hal, item), HALComponent):
                hal.message = hal.message + "\\n\\t" + str(item)

    def help_component(self, hal, component):
        for item in dir(component):
            if item.startswith("action") and callable(getattr(component, item)):
                hal.message = hal.message + "\\n\\t" + item.replace("action_", "")
