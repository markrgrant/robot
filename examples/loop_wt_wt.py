"""
A sample transfer protocol that uses nested loops for execution
"""
from collections import OrderedDict

from robot import Robot


robot = None

def transfer_tetradecane(sample):
    aspirate_tet_vol_in_ml = 0.251  # .250 but aspirate a little more
    tetradecane = robot.get_container('tetradecane', 0, 0)
    robot.aspirate(tetradecane, aspirate_tet_vol_in_ml)

def dispense_tetradecane(intermediate):
    dispense_vol_in_ml = 0.125
    robot.weigh(intermediate)
    robot.uncap(intermediate)
    robot.dispense(intermediate, dispense_vol_in_ml)
    robot.cap(intermediate)
    robot.weigh(intermediate)

def transfer_sample(sample):
    aspirate_vol_in_ml = 0.251 # .250 but aspirate a little more
    robot.aspirate(sample, aspirate_vol_in_ml)
    robot.wash_tip()  # wash after dispenses performed

def dispense_sample(intermediate):
    dispense_vol_in_ml = 0.125
    robot.uncap(intermediate)
    robot.dispense(intermediate, dispense_vol_in_ml)
    robot.cap(intermediate)
    robot.weigh(intermediate)

def transfer_hexane_intermediate(intermediate):
    aspirate_vol_in_ml = 16.6 # extra
    dispense_vol_in_ml = 16.5
    hexane = robot.get_container('hexane', 0, 0)
    robot.aspirate(hexane, aspirate_vol_in_ml)
    robot.uncap(intermediate)
    robot.dispense(intermediate, dispense_vol_in_ml)
    robot.cap(intermediate)
    robot.blow_off()

def transfer_sample_final(intermediate):
    aspirate_vol_in_ml = 0.06
    dispense_vol_in_ml = 0.05
    final = triton.getitem(intermediate, 'destinations', 0)
    robot.vortex(intermediate)
    robot.uncap(intermediate)
    robot.aspirate(intermediate, aspirate_vol_in_ml)
    robot.cap(intermediate)
    robot.uncap(final)
    robot.dispense(final, dispense_vol_in_ml)
    robot.cap(final)

def transfer_hexane_final(intermediate):
    aspirate_vol_in_ml = 1.46 # extra
    dispense_vol_in_ml = 1.45
    final = triton.getitem(intermediate, 'destinations', 0)
    hexane = robot.get_container('hexane', 0, 0)
    robot.aspirate(hexane, aspirate_vol_in_ml)
    robot.uncap(final)
    robot.dispense(final, dispense_vol_in_ml)
    robot.cap(final)
    robot.blow_off()

def wt_wt_prep_plan(bot, num_samples):
    global robot
    robot = robot = bot
    num_samples=10
    samples = robot.get_samples(num_samples)
    robot.create_container('hexane', 0, 0, 500.)
    robot.create_container('tetradecane', 0, 0, 500.)
    robot.prime()


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
            'syringe': {'max_volume_in_ml': 20.0}
        }
    }
    robot = Robot(config)
    NUM_SAMPLES = 10
    wt_wt_prep_plan(robot, NUM_SAMPLES)
