from container import Container
from material_container import MaterialContainer


class Arm(object):
    """An Arm is a robotic arm with a head that contains a Gripper and a
    Syringe.

    The Gripper is used to move Vials.  The Syringe is used to move
    material between MaterialContainers."""

    def __init__(self, config):
        self._gripper = Arm.Gripper(config['gripper'])
        self._syringe = Arm.Syringe(config['syringe'])

    def to_dict(self):
        return dict(
            gripper=self._gripper.to_dict(),
            syringe=self._syringe.to_dict(),
        )

    def wash_tip(self):
        """Washes the syringe.

        The syringe should be washed between aspirations of different
        materials.
        """
        return self._syringe.wash_tip()

    def prime(self):
        """Primes the syringe.

        The syringe should be primed at the start of a robot
        run.  This also washes the syringe.
        """
        return self._syringe.prime()

    @property
    def is_primed(self):
        return self._syringe.is_primed

    def aspirate(self, container, volume_in_ml):
        """Retrieve the given volume of material in ml from the specified
        container.
        """
        return self._syringe.aspirate(container, volume_in_ml)

    def dispense(self, container, volume_in_ml):
        """Dispense the given volume in ml into the given container."""
        return self._syringe.dispense(container, volume_in_ml)

    def to_str(self, indent=''):
        return indent + "Arm:\n\n{0}\n\n{1}\n\n{2}".format(
            self._gripper._contents.to_str(indent + '  ') if
            self._gripper._contents else indent + '  ' + 'vial=None',
            self._syringe.to_str(indent + '  '),
            indent + '  ' + self._syringe.to_str()
        )

    class Gripper(Container):
        """A gripper is a part of an Arm and is used to grab vials.  A gripper
        can hold only one vial at a time."""

        def __init__(self, config):
            self._contents = None
            super(Arm.Gripper, self).__init__('gripper')

        def to_dict(self):
            return dict(
                contents=self._contents
            )

    class Syringe(MaterialContainer):
        """A Syringe contains 0 or more materials.  An Arm contains a single
        Syringe."""
        def __init__(self, config):
            self._primed = False
            self._washed = False
            self.max_volume_in_ml = config['max_volume_in_ml']
            self._blown_off = False
            super(Arm.Syringe, self).__init__(
                'syringe', self.max_volume_in_ml)

        def to_dict(self):
            return dict(
                is_primed=self.is_primed,
                is_washed=self.is_washed,
                is_blown_off = self._blown_off,
                contents=self._contents
            )

        def wash_tip(self):
            if self._washed:
                raise SyringeAlreadyWashed("syringe already washed")
            self._washed = True

        def blow_off(self):
            """Any leftover material going into a vial that shouldn't be there
            is bad.  This is always done after washing."""
            if self._blown_off:
                raise SyringeBlownOff("syringe already blown off")
            self._blown_off = True

        def prime(self):
            if self._primed is True:
                raise SyringeAlreadyPrimed("syringe already primed")
            self._primed = True

        def aspirate(self, container, volume_in_ml):
            if self._primed is False:
                raise SyringeNotPrimed()
            self.transfer(container, volume_in_ml)
            self._washed = False
            self._blown_off = False

        def dispense(self, container, volume_in_ml):
            if self.is_empty is True:
                raise SyringeEmpty()
            container.transfer(self, volume_in_ml)

        @property
        def is_blown_off(self):
            return self._blown_off is True

        @property
        def is_washed(self):
            return self._washed is True

        @property
        def is_primed(self):
            return self._primed is True

        def to_str(self, indent=''):
            return indent + "Syringe: contents={0}, primed={1}".format(
                self._contents, self._primed)


class SyringeNotWashed(Exception):
    pass

class SyringeAlreadyWashed(Exception):
    pass

class SyringeAlreadyPrimed(Exception):
    pass

class SyringeNotPrimed(Exception):
    pass

class SyringeEmpty(Exception):
    pass

class GripperBusy(Exception):
    pass

class GripperEmpty(Exception):
    pass

class SyringeBlownOff(Exception):
    pass
