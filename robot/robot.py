"""
A liquid transfer robot simulator
"""
from collections import OrderedDict

from arm import Arm
from rack import Rack
from capper import Capper
from reader import Reader
from balance import Balance
from vortexer import Vortexer
from position import Position
from bottle import Bottle
from vial import Vial


class Robot(object):
    """
    The Robot class simulates a real-world robot. The robot itself
    is made up of a set of components:
        - Arm
          - Gripper(s)
          - Syringe
        - Capper
        - Balance
        - Reader
        - Vortexer
        - Rack(s).  Each rack holds a particular type of
          container and has m-by-n positions where each position can hold
          1 container of the given type.

          An example of the types of containers that might be in use on
          a Robot are:
          - 20 ml scint containers
          - 2 ml GC containers
          - bottle of Tetradecane (internal standard)
          - bottle of Hexane

    The Robot class wraps these components and provides a simplified
    interface for executing tasks on the robot.
    """
    def __init__(self, config):
        """
        Create the components and the rack dimensions of the Robot.
        The config argument contains the types and dimensions of the racks.

        Args:
            config (dict): A dict of the form

            {
                'racks': {
                    'container_type_a': {x: 10, y: 20},
                    'container_type_b': {x: 10, y: 20}
                },
                'vortexer': {'container_types': ['gc_vial']},
                'capper': {'container_types': ['gc_vial']},
                'arm: {
                    'gripper': {},
                    'syringe': {'max_volume_in_ml': 2}
                }
            }

        Returns:
            (Robot): a new Robot instance
        """
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

        self._capper   = Capper(**config['capper'])
        self._balance  = Balance()
        self._arm      = Arm(config['arm'])
        self._reader   = Reader()
        self._vortexer = Vortexer(**config['vortexer'])
        self._racks    = dict()

        for k, v in config['racks'].items():
            self._racks[k] = Rack(k, v['x'], v['y'])

        self.create_container('hexane', 0, 0, 500.)
        self.create_container('tetradecane', 0, 0, 500.)

    def create_container(self, rack_name, x_pos, y_pos, volume_in_ml):
        container = Bottle(rack_name)
        container.add_contents(rack_name=volume_in_ml)
        container.position = Position(x_pos, y_pos)
        self.add_container(container)
        return container

    def get_container(self, rack_name, x_pos, y_pos):
        return self._racks[rack_name]._containers[x_pos][y_pos]

    def get_samples(self, num_samples):
        def create_sample(index):
            def create_final(index):
                container = Vial('final')
                container.position = Position(index, 0)
                self.add_container(container)
                return container
            def create_intermediate(index):
                container = Vial('intermediate')
                container.position=Position(index, 0)
                container.destinations=[create_final(index)]
                self.add_container(container)
                return container
            container = Vial('sample')
            container.position=Position(index, 0)
            container.add_contents(sample=1.0)
            container.destinations=[
                create_intermediate(index*2),
                create_intermediate(index*2+1)
            ]
            self.add_container(container)
            return container
        return [create_sample(i) for i in range(0, num_samples)]

    def prime(self):
        """
        Prepares the syringe for aspirating a precise amount of
        material.

        Raises:
            SyringeAlreadyPrimed
        """
        print "prime syringe with hexane"
        self._arm.prime()

    def wash_tip(self):
        """
        Cleans the syringe of contaminating material.

        Raises:
            SyringeAlreadyWashed
        """
        print "wash tip"
        self._arm.wash_tip()

    def blow_off(self):
        """
        Removes any excess liquid droplets from the syringe that
        may be present after washing.

        Raises:
            SyringeBlownOff
        """
        print "blow off tip"
        self._arm._syringe.blow_off()

    def vortex(self, container):
        """
        mix the container
        """
        print "vortex {0}".format(container)
        self._racks[
            container.container_type].remove_container(container)
        self._vortexer.add_container(container)
        self._vortexer.vortex()
        self._vortexer.remove_container()
        self._racks[container._container_type].add_container(container)

    def cap(self, container):
        """
        Cap the container.

        Args:
            container (Container): The container to be capped

        Raises:
            CapperOccupied
            CapperNoCap
     """
        print "cap {0}".format(container)
        self._racks[
            container.container_type].remove_container(container)
        self._capper.add_container(container)
        self._capper.cap()
        self._capper.remove_container()
        self._racks[
            container.container_type].add_container(container)

    def uncap(self, container):
        """
        Uncap the container.

        Args:
            container (Container): The container to be uncapped
        Returns:
            None

        Raises:
            CapperContainerType
            CapperOccupied
            CapperHasCap
        """
        print "uncap {0}".format(container)
        self._racks[
            container.container_type].remove_container(container)
        self._capper.add_container(container)
        self._capper.uncap()
        self._capper.remove_container()
        self._racks[
            container.container_type].add_container(container)


    def transfer(self, source_container, dest_container, volume_in_ml):
        self.aspirate(source_container, volume_in_ml)
        self.dispense(dest_container, volume_in_ml)

    def weigh(self, container):
        """
        Weigh the container and return a sample object with its weight
        assigned.

        Args:
            container (dict): A dict of the form
            {
                "container_type": <str>,
                "position":
        """
        print "weigh {0}".format(container)
        self._racks[
            container.container_type].remove_container(container)
        self._balance.add_container(container)
        container.weight = self._balance.weigh_container()
        self._balance.remove_container()
        weighed_container = self._racks[
            container.container_type].add_container(container)
        return weighed_container

    def aspirate(self, container, volume_in_ml):
        print "aspirate {0} ml from {1}".format(volume_in_ml, container)
        self._arm._syringe.aspirate(container, volume_in_ml)

    def dispense(self, container, volume_in_ml):
        print "dispense {0} ml into {1}".format(volume_in_ml, container)
        self._arm._syringe.dispense(container, volume_in_ml)

    def add_container(self, container):
        self._racks[container.container_type].add_container(container)

    def read_barcode(self, container):
        self._racks[
            container.container_type].remove_container(container)
        self._reader.add_container(container)
        self._reader.read_barcode()
        self._reader.remove_container()
        container = self._racks[
            container.container_type].add_container(container)

    def to_dict(self):
        return dict(
            capper=self._capper.to_dict(),
            balance=self._balance.to_dict(),
            arm=self._arm.to_dict(),
            reader=self._reader.to_dict(),
            vortexer=self._vortexer.to_dict(),
            racks=[v.to_dict() for v in self._racks.itervalues()]
        )


    def to_str(self):
        """
        Provides a string representation of the state of the Robot at the time
        that the method is called.

        Returns:
            (string): a string representation of the state of the Robot
        """
        return self._to_str('')

    def _to_str(self, indent):
        rack_info = ""
        for rack_type, rack in self._racks.iteritems():
            rack_info += rack.to_str(indent + '  ')
        rack_info = indent + "\n\n{0}".format(rack_info)

        return "Robot:\n\n{0}\n\n{1}\n\n{2}\n\n{3}".format(
            self._capper.to_str(indent + '  '),
            rack_info,
            self._balance.to_str(indent + '  '),
            self._arm.to_str(indent + '  '),
            self._reader.to_str(indent + '  ')
        )
