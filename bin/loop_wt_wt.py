"""
A version of the wt/wt protocol that uses a sequence of nested loops for executing a
wt/wt protocol.

Notes:
sample vial is also known as the source vial (vial type = GC vial)
intermediate vial is also known as the dilution vial  (vial type = 'scint vial')
final vial (vial type= GC vial)
"""
import triton

anabot = None

def transfer_tetradecane(sample):
    aspirate_tet_vol_in_ml = 0.21
    tetradecane = anabot.get_tetradecane()
    anabot.aspirate(tetradecane, aspirate_tet_vol_in_ml)
    destinations = triton.getattr(sample, 'destinations')
    triton.map(dispense_tetradecane, destinations)

def dispense_tetradecane(intermediate):
    dispense_vol_in_ml = 0.10
    anabot.weigh(intermediate)
    anabot.uncap(intermediate)
    anabot.dispense(intermediate, dispense_vol_in_ml)
    anabot.cap(intermediate)
    anabot.weigh(intermediate)

def transfer_sample(sample):
    aspirate_vol_in_ml = 0.21
    anabot.aspirate(sample, aspirate_vol_in_ml)
    destinations = triton.getattr(sample, 'destinations')
    triton.map(dispense_sample, destinations)
    anabot.wash_tip()

def dispense_sample(intermediate):
    dispense_vol_in_ml = 0.10
    anabot.uncap(intermediate)
    anabot.dispense(intermediate, dispense_vol_in_ml)
    anabot.cap(intermediate)
    anabot.weigh(intermediate)

def dilute_sample(sample):
    destinations = triton.getattr(sample, 'destinations')
    triton.map(transfer_hexane, destinations)
    triton.map(transfer_final, destinations)

def transfer_hexane(intermediate):
    aspirate_vol_in_ml = 0.11
    dispense_vol_in_ml = 0.10
    hexane = anabot.get_hexane()
    anabot.aspirate(hexane, aspirate_vol_in_ml)
    anabot.uncap(intermediate)
    anabot.dispense(intermediate, dispense_vol_in_ml)
    anabot.cap(intermediate)
    anabot.blow_off()

def transfer_final(intermediate):
    aspirate_vol_in_ml = 0.11
    dispense_vol_in_ml = 0.10
    anabot.vortex(intermediate)
    anabot.uncap(intermediate)
    anabot.aspirate(intermediate, aspirate_vol_in_ml)
    anabot.cap(intermediate)
    final = triton.getitem(intermediate, 'destinations', 0)
    anabot.uncap(final)
    anabot.dispense(final, dispense_vol_in_ml)
    anabot.cap(final)

def wt_wt_prep_plan(bot, num_samples):
    global anabot
    anabot = bot
    samples = anabot.get_samples(num_samples)
    anabot.prime()
    triton.map(transfer_tetradecane, samples)
    triton.map(transfer_sample, samples)
    triton.map(dilute_sample, samples)


if __name__ == '__main__':
    wt_wt_prep_plan(10)
