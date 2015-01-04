from material_container import MaterialContainer
from barcoded import Barcoded


class Bottle(Barcoded, MaterialContainer):
    """
    A bottle is a type of material container designed to hold a large
    reservoir of a bulk reagent such as water or a diluent.

    It has a maximum volume of 500 mls.  It is typically too large to be
    moved by a robotic arm but rather remains stationary and liquid is
    drawn off by a syringe.
    """
    MAX_VOLUME_IN_ML = 500

    def __init__(self, container_type):
        return super(Bottle, self).__init__(
            container_type,
            max_volume_in_ml=self.MAX_VOLUME_IN_ML,
        )
