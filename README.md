# Liquid Transfer Robot Simulator

The automated preparation of liquid samples in biotechnology is a huge
timesaver.  However the optimal preparation of samples often involves
many steps of different kinds such as the transfer of liquids,
vortexing and centrifugation of vials, and OD measurement.  Furthermore, 
these steps must be executed in such a way as to ensure that they are
performed in the correct order and without cross-contamination of samples
or reagents. 

The purpose of this package is to provide a liquid transfer robot
simulator for the validation of robot configurations (which specify the types
of components in the robot) and the validation of scripts that drive 
robots with those configurations.

Should any action be performed in the execution of a simulation that could
result in contamination of a sample or reagent, or depletion of the remaining
volume of a container, or be physically impossible such as placing two samples
in the same position in a rack, an exception will be thrown when the
simulation is run.  The state of the robot during the execution of a simulation
is printed to standard output and the volumes can be inspected for 
correctness.

## Setup

To begin using the package, navigate to the root directory of the robot
project (the same directory containing setup.py) and create a virtual
environment:
```
% virtualenv robotenv
```

Activate the virtual environment.  This should be done whenever the
package is to be used: 

```
% source robotenv/bin/activate
```

Install the robot package:
```
(robotenv) % python setup.py install
```

Run an example script: 
```
(robotenv) % python examples/loop_wt_wt.py
```


## Usage

To use the installed robot package, write a Python script that:

1. Defines a robot configuration that specifies the locations of vials,
   the reagents to be used and their initial volumes.
2. Creates a robot object using the configuration from step 1
3. Executes the desired steps on the simulation.  This will be a sequence
   of steps such as transfers, weighs, mixing, and so on.

### Defining a Robot Configuration

A robot configuration specifies the components in the robot and their
dimensions and is required in order to create a new Robot object.
For example, the following configuration specifies a robot with a number
of different racks of various x and y dimensions, a vortexer, a capper for
capping and uncapping vials, and an arm for moving vials and transferring
samples:

```
config = {
    'racks': OrderedDict([
        ('sample', {'x': 10, 'y': 3}),
        ('intermediate', {'x': 20, 'y': 5}),
        ('final', {'x': 20, 'y': 5}),
        ('tetradecane', {'x': 1, 'y': 1}),
        ('hexane', {'x': 1, 'y': 1})
    ]),
    'vortexer': {'container_types': ['sample', 'intermediate', 'final']},
    'capper': {'container_types': ['sample', 'intermediate', 'final']},
    'arm': {
        'gripper':{},
        'syringe': {'max_volume_in_ml': 2}
    }
}
```

### Creating a Robot Instance

The Robot class takes a configuration object and creates a 
Robot object.  Methods are then called on this robot object in order to
move vials, transfer liquids, etc.

```
robot = Robot(config)
```

### Defining Samples and Performing Actions

```
samples = robot.load_samples(num_samples)
hexane = robot.get('hexane', 0, 0)
robot.uncap(samples[0])
robot.aspirate(hexane, 0.5)
robot.dispense(samples[0], 0.45)
robot.cap(samples[0])
```

Other methods are provided that are present in any liquid transfer robot, 
such as: 

```
robot.transfer(source, dest, vol_in_ml)
robot.weigh(container)
robot.prime()
robot.wash()
robot.blow_off()
robot.mix(vial)
```
## Additional Examples

More detailed examples are provided in the examples directory. To run
one of the examples from the root directory, make sure the virtual environment
is enabled and then run: 
```
(robotenv) % python examples/loop_wt_wt.py
```

## Running Tests

Nosetests can be used to run the unit tests:
```
% nosetests
```

## TODO

A simple DSL for specifying configurations and defining the actions to be
taken would simplify validation.

Documentation on the full set of pre-defined robot components and their
arguments is needed.

It would be ideal if protocols could be generated given constraints rather 
than just tested for validity.
