## Summary

A liquid transfer robot simulator

## usage

### define a robot instance with a configuration
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
robot = Robot(config)
```

### define samples and perform liquid transfers

    samples = robot.load_samples(num_samples)

    hexane = robot.get('hexane', 0, 0)
    robot.uncap(samples[0])
    robot.aspirate(hexane, 0.5)
    robot.dispense(samples[0], 0.45)
    robot.cap(samples[0])

### other methods

- transfer(source, dest, vol_in_ml)
- weigh(container)
- prime()
- wash()
- blow_off()
- mix(vial)

