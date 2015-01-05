"""
Commands that can be executed by the Robot.
"""
from container import Container
from util import barcode_iterator

def get_hexane():
    return Container(
        rack='hexane',
        position=0,
        barcode='Hexane'
    )

def get_tetradecane():
    return Container(
        rack='tetradecane',
        position=0,
        barcode='Tetradecane'
    )

def get_samples(num_samples):
    # read the sample barcodes and return sample
    # objects for each
    def create_sample(index):

        def create_final(index):
            return Container(
                rack='final',
                position=index,
                barcode=next(barcode_iterator)
            )
        # this isn't entirely general, because of 'sample' input
        def create_intermediate(index):
            return Container(
                rack='intermediate',
                position=index,
                barcode=next(barcode_iterator),
                destinations=[
                    create_final(index)
                ]
            )
        return Container(
            rack='sample',
            position=index,
            barcode=next(barcode_iterator),
            destinations=[
                create_intermediate(index*2),
                create_intermediate(index*2+1)
            ]
        )
    return [create_sample(i) for i in range(0, num_samples)]


def weigh(container):
    print "weigh {0}".format(container)
    container.weight = 1.0
    return container


def uncap(container):
    print "uncap {0}".format(container)


def dispense(dest_container):
    # this occurs after an aspirate
    print "dispense into {0}".format(dest_container)


def wash_tip():
    print "wash tip"


def prime():
    """primes the syringe pump by removing air from the
    syringe line.  It may also wash the tip.  Priming is
    done once at the start of a robot run because air
    can appear in a robot. Hexane is used as the priming
    reagent"""
    print "prime syringe with hexane"

def aspirate(container):
    """aspiration is drawing liquid to be dispensed into
    the syringe.  There is a maximum volume that can be
    stored so this might determine the number of dispenses
    that can be performed for a given aspirate."""
    print "aspirate from {0}".format(container)


def cap(container):
    # DONE
    print "cap {0}".format(container)


def vortex(container):
    # DONE
    print "vortex {0}".format(container)


def blow_off():
    # DONE
    print "blow off tip"


def to_dict():
    # DONE
    return dict()
