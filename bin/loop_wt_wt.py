"""
A sample transfer protocol that uses nested loops for execution

Notes:
sample vial is also known as the source vial (vial type = GC vial)
intermediate vial is also known as the dilution vial  (vial type = 'scint vial')
final vial (vial type= GC vial)
"""
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

def wt_wt_prep_plan(bot, num_samples):
    global robot
    robot = bot
    samples = robot.get_samples(num_samples)
    robot.prime()
    triton.map(transfer_tetradecane, samples)
    triton.map(transfer_sample, samples)
    triton.map(dilute_sample, samples)


if __name__ == '__main__':
    robot = Robot()
    wt_wt_prep_plan(robot, 10)
