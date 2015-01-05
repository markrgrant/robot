"""
A version of an robot wt/wt protocol that uses continuations
rather than loops for determining the sequence of commands that
are executed.
"""
from robot import Robot

robot = Robot()


def replicate_plan(sample, replicate):
    hexane = robot.get_hexane()
    aspirate_vol_in_ml = 0.11
    robot.weigh(replicate)
    robot.uncap(replicate)
    robot.dispense(replicate)
    robot.cap(replicate)
    robot.weigh(replicate)
    yield
    robot.uncap(replicate)
    robot.dispense(replicate)
    robot.cap(replicate)
    robot.weigh(replicate)
    yield
    #robot.add_hexane(replicate)
    robot.aspirate(hexane)
    robot.uncap(replicate)
    robot.dispense(replicate)
    robot.cap(replicate)
    yield
    robot.vortex(replicate)
    robot.uncap(replicate)
    robot.aspirate(replicate)
    robot.cap(replicate)
    final = replicate.destinations[0]
    robot.uncap(final)
    robot.dispense(final)
    robot.cap(final)
    yield


def sample_plan(sample):
    intermediates = sample.destinations
    tetradecane = robot.get_tetradecane()
    replicate_plans = [replicate_plan(sample, di) for di in intermediates]
    robot.aspirate(tetradecane)
    [next(wf) for wf in replicate_plans]
    yield
    robot.aspirate(sample)
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
    sample_plans = [sample_plan(sa) for sa in samples]
    [next(wf) for wf in sample_plans]
    robot.wash_tip()
    [next(wf) for wf in sample_plans]
    [next(wf) for wf in sample_plans]


# run the root plan with a specified number of samples
NUM_SAMPLES = 10
wt_wt_prep_plan(10)
