"""
A version of a robot protocol that uses continuations
rather than loops for determining the sequence of commands that
are executed.
"""
from collections import OrderedDict

from robot import Robot


robot = None

def replicate_plan(sample, replicate):

    hexane = robot.get_container('hexane', 0, 0)
    aspirate_vol_in_ml = 0.10
    dispense_vol_in_ml = 0.10
    robot.weigh(replicate)
    robot.uncap(replicate)
    robot.dispense(replicate, dispense_vol_in_ml)
    robot.cap(replicate)
    robot.weigh(replicate)
    yield
    robot.uncap(replicate)
    robot.dispense(replicate, dispense_vol_in_ml)
    robot.cap(replicate)
    robot.weigh(replicate)
    yield
    robot.aspirate(hexane, aspirate_vol_in_ml)
    robot.uncap(replicate)
    robot.dispense(replicate, dispense_vol_in_ml)
    robot.cap(replicate)
    yield
    robot.vortex(replicate)
    robot.uncap(replicate)
    robot.aspirate(replicate, aspirate_vol_in_ml)
    robot.cap(replicate)
    final = replicate.destinations[0]
    robot.uncap(final)
    robot.dispense(final, dispense_vol_in_ml)
    robot.cap(final)
    yield


def sample_plan(sample):
    aspirate_vol_in_ml = 0.21
    intermediates = sample.destinations
    tetradecane = robot.get_container('tetradecane', 0, 0)
    replicate_plans = [replicate_plan(sample, di) for di in intermediates]
    robot.aspirate(tetradecane, aspirate_vol_in_ml)
    [next(wf) for wf in replicate_plans]
    yield
    robot.aspirate(sample, aspirate_vol_in_ml)
    [next(wf) for wf in replicate_plans]
    robot.wash_tip()
    yield
    [next(wf) for wf in replicate_plans]
    robot.blow_off()
    [next(wf) for wf in replicate_plans]
    yield


def wt_wt_prep_plan(num_samples):
    robot.prime()
    samples = robot.get_samples(num_samples)
    robot.create_container('hexane', 0, 0, 500.)
    robot.create_container('tetradecane', 0, 0, 500.)
    sample_plans = [sample_plan(sa) for sa in samples]
    [next(wf) for wf in sample_plans]
    robot.wash_tip()
    [next(wf) for wf in sample_plans]
    [next(wf) for wf in sample_plans]


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
        'capper': {'container_types': ['sample', 'intermediate', 'final']},
        'arm': {
            'gripper':{},
            'syringe': {'max_volume_in_ml': 2}
        }
    }
    global robot
    robot = Robot(config)
    NUM_SAMPLES = 10
    wt_wt_prep_plan(NUM_SAMPLES)
