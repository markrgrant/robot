from material_container import MaterialContainer
from barcoded import Barcoded
from capped import Capped


class Vial(Barcoded, Capped, MaterialContainer):
    """
    A Vial is a container of material that also:

    1. Has a cap
    3. Is barcoded
    """
    MAX_VOLUME_IN_ML = 20

    def __init__(self, container_type):
        self._mixed = False
        super(Vial, self).__init__(
            container_type,
            max_volume_in_ml=self.MAX_VOLUME_IN_ML)

    def mix(self):
        self._mixed = True

    @property
    def is_mixed(self):
        return self._mixed == True

    def cap(self):
        if self.is_capped:
            raise VialCapped()
        self._capped = True

    def uncap(self):
        if self.is_capped is False:
            raise VialUncapped()
        self._capped = False

    @property
    def is_capped(self):
        return self._capped == True

    def add_contents(self, **contents):
        self._mixed = False
        super(Vial, self).add_contents(**contents)

    def remove_contents(self, volume_in_ml):
        if self.is_mixed is False and len(self._contents.keys()) > 1:
            raise VialUnmixed()
        return super(Vial, self).remove_contents(volume_in_ml)

    def to_str(self, indent=''):
        return indent + "Vial(container_type='{0}', is_capped={1}, is_mixed={2})".format(
            self._container_type,
            self._capped,
            self._mixed)


class VialCapped(Exception):
    pass

class VialUncapped(Exception):
    pass

class VialUnmixed(Exception):
    pass
