"""
A version of an anabot wt/wt protocol that uses continuations
rather than loops for determining the sequence of commands that
are executed.
"""
from anabot import Anabot

anabot = Anabot()


def replicate_plan(sample, replicate):
    hexane = anabot.get_hexane()
    aspirate_vol_in_ml = 0.11
    anabot.weigh(replicate)
    anabot.uncap(replicate)
    anabot.dispense(replicate)
    anabot.cap(replicate)
    anabot.weigh(replicate)
    yield
    anabot.uncap(replicate)
    anabot.dispense(replicate)
    anabot.cap(replicate)
    anabot.weigh(replicate)
    yield
    #anabot.add_hexane(replicate)
    anabot.aspirate(hexane)
    anabot.uncap(replicate)
    anabot.dispense(replicate)
    anabot.cap(replicate)
    yield
    anabot.vortex(replicate)
    anabot.uncap(replicate)
    anabot.aspirate(replicate)
    anabot.cap(replicate)
    final = replicate.destinations[0]
    anabot.uncap(final)
    anabot.dispense(final)
    anabot.cap(final)
    yield


def sample_plan(sample):
    intermediates = sample.destinations
    tetradecane = anabot.get_tetradecane()
    replicate_plans = [replicate_plan(sample, di) for di in intermediates]
    anabot.aspirate(tetradecane)
    [next(wf) for wf in replicate_plans]
    yield
    anabot.aspirate(sample)
    [next(wf) for wf in replicate_plans]
    anabot.wash_tip()
    yield
    [next(wf) for wf in replicate_plans]
    anabot.blow_off()
    [next(wf) for wf in replicate_plans]
    yield


def wt_wt_prep_plan(num_samples):
    anabot.prime()
    samples = anabot.get_samples(num_samples)
    sample_plans = [sample_plan(sa) for sa in samples]
    [next(wf) for wf in sample_plans]
    anabot.wash_tip()
    [next(wf) for wf in sample_plans]
    [next(wf) for wf in sample_plans]


# run the root plan with a specified number of samples
NUM_SAMPLES = 10
wt_wt_prep_plan(10)
