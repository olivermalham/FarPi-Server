# FarPi

Welcome to FarPi! FarPi is a lightweight server that allows you to remote control hardware attached to a Raspberry Pi via any modern web browser. It is designed so that new virtual control panels can be setup with a minimum of code writing. Although FarPi is written in Python, you don't need any previous python experience, just copy and paste from the examples to get started.

## Quick Start
Running FarPi is very easy. Fire up your Raspberry Pi, open a shell (command line). Navigate to the directory where you installed FarPi and run these commands:

```
cd server/
python far_pi.py all_pi_app
```

Then open a web browser on the Pi, and go to:

```
http://localhost:8888/
```

And you should see the basic panel that lets you contol all the Pi's GPIO pins via toggle switches. Because FarPi runs as a webserver, you can access your control panel from anywhere in the world, as long as you have configured your networking appropriately (too big a subject for this little readme file!).

## How It Works
FarPi is built on top of the Tornado threadless web server. The panel webpage is generated dynamically by the server and sent to the client web browser. The panel on the browser uses a websocket connection back to the server so it can process two way information flow without having to reload the page each time, or use heavyweight REST operations. FarPi can support multiple users on the same panel at the same time, with all panels being updated more or less in real-time. So if User A flicks a toggle switch from off to on, User B will see the same toggle switch move by itself to on. The server reads the state of the hardware periodically, by default every 500ms, and sends to each client a JSON datastructure which the client code uses to update the user interface. Due to the lightweight nature of the system, even a little computer like the Pi should be able to support a few dozen users at the same time (FarPi hasn't been stress tested though, so this may not hold).

## Code Structure
FarPi is split into a number of software components that have specific jobs.

### Application File
The application file holds all the other components together. It serves as the primary configuration file for a control panel. You should have one application file for each control panel that you set up. Here is a basic application file:

```python
# Import the default settings from base_app
from apps.base_app import *

# The Hardware Abstraction Layer (HAL) package represents the hardware attached to the server
# that the user will interact with via the UI
from HAL.basic_pi import BasicPi

# Number of milliseconds to delay between updates to clients
refresh_ms = 500

# Create the HAL object that interfaces with the hardware
hal = BasicPi()
```

As you can see, there is not much to it. To customise to your own project, first change the import statement for the HAL module you want to use. Change the refresh delay if you want, but bear in mind that reducing the size of this delay will increase network traffic and load on the Raspberry Pi's processor. Change the line that creates the hal object so it matches the custom HAL you want to use. Finally, change "example_ui" to what ever user interface module you want to use. The HAL and UI modules are decribed below.

### HAL - Hardware Abstraction Layer
The HAL objects create the bridge between the FarPi server and the actual Raspberry Pi hardware. They are all stored in the HAL subdirectory. A base class in hal.py defines the basic functionality. The important files in this folder are:

#### hal.py
This contains the code that defines the basic functionality of the HAL system. If you are going to write your own custom HAL, read the documentation in this file. Your custom HAL should subclass the `HAL` class in here, and your custom components should subclass the `HALComponent` class.


#### basic_pi.py
The file defines a single `HALComponent`, `BasicPiGPIO`, which represents a basic GPIO pin. Direction can be set to in or out, pull up or down and pin number are all configurable. Uses the GPIO module from the RPi library.

The `BasicPi` HAL class defined here just makes available all GPIO pins as outputs with no pull-ups or downs. Uses the BCM pin numbering scheme.

#### virtual.py
The virtual module contains a bunch of HALComponents that provide advanced logic and behaviour. This is only a quick overview, check the source code comments for detailed info. 

`Group` is not a component, it's a helper class that lets you group multiple HALComponent names together. Primarily used to make the HAL object declarations syntax cleaner.

`GroupToggle` lets you switch a group of other HALComponnents between two sets of pre-defined values.

`GeneratorSawTooth` simulates a saw-tooth waveform between a lower and upper bound. Steps by a delta value on every update, so frequemcy is dependant on the refresh interval you set in your app file.

`TripWire` is similar to `GroupToggle`, except that it switches when the value of another HALComponent crosses a threshold value. Could be used for instance to turn on a couple of cooling fans if a temperature sensor passes 30 degrees.

`IfThisThen` is a very powerful virtual component. Using it requires a bit more Python knowledge than the others. Every refresh, it evaluates a "this" expression. If "this" evaluates to True, the "then" expression is executed. If "this" evaluates to False, the "otherwise" expression is executed. All of these expressions are fragments of Python code that are executed using the parent HAL object as the namespace.

#### servo.py
This file provides a small extension to the BasicHAL module so that R/C servoes can be controlled from any GPIO pin. It uses the Python bindings for the PiGPIO library. If you have a project that uses R/C servoes, you'll want to use `ServoHAL` as the base class for your own HAL. Two components are provided:

`Servo` - a basic interface to a single servo on a GPIO pin. Allows the position to be set to any arbitary point, or toggle the position between the two end points. The end points are configurable for maximum flexibility.

`IndexedServo` - similar to the basic Servo component, but is initialise with a list of preset positions. The servo can then be toggle up or down and it will move through the positions defined in the list. It can also be set to any one of the preconfigured positions without stepping through the intermediate positions.


## ToDo
FarPi is still in the very early stages of development, and there is much left to do. Off the top of my head:

1. Create components to handle both Waveshare round LCD and Pimoroni display hat mini
2. Create a component to handle thermal imaging sensor
3. Create a component to handle VX???? ToF ranging sensor
4. Create a component to handle ????? motion platform
5. Create a component to handle serial GPS module
6. Create a pipfile and get the code into a decent shape for others to use
7. Review documentation
8. Complete review, cleanup and refactor of the camera streams system
9. 