"""
A sample transfer protocol that uses nested loops for execution
"""
from collections import OrderedDict

from robot import Robot


robot = None

def transfer(sources, destinations, vol_in_ml, wash=False, weigh=False, vortex=False):
    factor = len(destinations)/len(sources)
    aspirate_vol_in_ml = factor * vol_in_ml + .01 # a head volume
    for i, source in enumerate(sources):
        if vortex is True:
            robot.vortex(source)
        robot.uncap(source)
        robot.aspirate(source, aspirate_vol_in_ml)
        robot.cap(source)
        for j in range(i*factor, i*factor + factor):
            dest = destinations[j]
            robot.uncap(dest)
            robot.dispense(dest, vol_in_ml)
            robot.cap(dest)
            if weigh:
                robot.weigh(destinations[j])
        if wash:
            robot.wash_tip()

def wt_wt_prep_plan(bot, num_samples):
    init_hex_vol_in_ml = 500.
    init_tet_vol_in_ml = 500.
    init_sample_vol_in_ml = 1.0
    tet_vol_in_ml = 0.1
    first_sample_vol_in_ml = 0.1
    second_sample_vol_in_ml = 0.1
    hexane_vol_in_ml = 0.1

    global robot
    robot = bot
    num_intermediates = num_samples * 2
    samples = robot.create_containers('sample', num_samples, init_sample_vol_in_ml, 'vial')
    intermediates = robot.create_containers('intermediate', num_intermediates, 0., 'vial')
    finals = robot.create_containers('final', num_intermediates, 0, 'vial')
    tetradecanes = robot.create_containers('tetradecane', 1, init_tet_vol_in_ml, 'bottle')
    hexanes = robot.create_containers('hexane', 1, init_hex_vol_in_ml, 'bottle')
    robot.prime()
    transfer(tetradecanes, intermediates, tet_vol_in_ml, wash=False, weigh=True)
    transfer(samples, intermediates, first_sample_vol_in_ml, wash=True, weigh=True)
    transfer(hexanes, finals, hexane_vol_in_ml, wash=False, weigh=False)
    transfer(intermediates, finals, second_sample_vol_in_ml, wash=True, weigh=False, vortex=True)


if __name__ == '__main__':
    config = {
        'racks': OrderedDict([
            ('sample', {'x': 10, 'y': 3}),
            ('intermediate', {'x': 20, 'y': 5}),
            ('final', {'x': 20, 'y': 5}),
            ('tetradecane', {'x': 1, 'y': 1}),
            ('hexane', {'x': 1, 'y': 1})
        ]),
        'vortexer': {'container_types': ['sample', 'intermediate', 'final']},
        'capper': {'container_types': ['tetradecane', 'hexane', 'sample', 'intermediate', 'final']},
        'arm': {
            'gripper':{},
            'syringe': {'max_volume_in_ml': 20}
        }
    }
    robot = Robot(config)
    NUM_SAMPLES = 10
    wt_wt_prep_plan(robot, NUM_SAMPLES)
