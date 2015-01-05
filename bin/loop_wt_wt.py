"""
A sample transfer protocol that uses nested loops for execution
"""
from collections import OrderedDict

import triton
from robot import Robot

robot = None

def transfer_tetradecane(sample):
    aspirate_tet_vol_in_ml = 0.21
    tetradecane = robot.get_tetradecane()
    robot.aspirate(tetradecane, aspirate_tet_vol_in_ml)
    destinations = triton.getattr(sample, 'destinations')
    triton.map(dispense_tetradecane, destinations)

def dispense_tetradecane(intermediate):
    dispense_vol_in_ml = 0.10
    robot.weigh(intermediate)
    robot.uncap(intermediate)
    robot.dispense(intermediate, dispense_vol_in_ml)
    robot.cap(intermediate)
    robot.weigh(intermediate)

def transfer_sample(sample):
    aspirate_vol_in_ml = 0.21
    robot.aspirate(sample, aspirate_vol_in_ml)
    destinations = triton.getattr(sample, 'destinations')
    triton.map(dispense_sample, destinations)
    robot.wash_tip()

def dispense_sample(intermediate):
    dispense_vol_in_ml = 0.10
    robot.uncap(intermediate)
    robot.dispense(intermediate, dispense_vol_in_ml)
    robot.cap(intermediate)
    robot.weigh(intermediate)

def dilute_sample(sample):
    destinations = triton.getattr(sample, 'destinations')
    triton.map(transfer_hexane, destinations)
    triton.map(transfer_final, destinations)

def transfer_hexane(intermediate):
    aspirate_vol_in_ml = 0.11
    dispense_vol_in_ml = 0.10
    hexane = robot.get_hexane()
    robot.aspirate(hexane, aspirate_vol_in_ml)
    robot.uncap(intermediate)
    robot.dispense(intermediate, dispense_vol_in_ml)
    robot.cap(intermediate)
    robot.blow_off()

def transfer_final(intermediate):
    aspirate_vol_in_ml = 0.11
    dispense_vol_in_ml = 0.10
    robot.vortex(intermediate)
    robot.uncap(intermediate)
    robot.aspirate(intermediate, aspirate_vol_in_ml)
    robot.cap(intermediate)
    final = triton.getitem(intermediate, 'destinations', 0)
    robot.uncap(final)
    robot.dispense(final, dispense_vol_in_ml)
    robot.cap(final)

def wt_wt_prep_plan(num_samples):
    samples = robot.get_samples(num_samples)
    robot.prime()
    triton.map(transfer_tetradecane, samples)
    triton.map(transfer_sample, samples)
    triton.map(dilute_sample, samples)


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
