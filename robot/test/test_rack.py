from ..rack import (
    Rack,
    RackContainerTypeInvalid,
    RackPositionInvalid,
    RackPositionOccupied
)
from ..container import Container
from ..position import Position
from nose.tools import raises

def test_rack():
    Rack('gc_vial', 3, 4)

def test_rack_add_container():
    rack = Rack('gc_vial', 3, 4)
    rack.add_container(Container('gc_vial', position=Position(0, 0)))

@raises(RackContainerTypeInvalid)
def test_rack_add_container_invalid_type():
    rack = Rack('gc_vial', 3, 4)
    # attempt to add a gc container to an invalid position
    rack.add_container(Container('scint_container', position=Position(0, 0)))

@raises(RackPositionOccupied)
def test_rack_add_container_occupied():
    rack = Rack('gc_vial', 3, 4)
    # attempt to add a gc container to an occupied position
    rack.add_container(Container('gc_vial', position=Position(0, 0)))
    rack.add_container(Container('gc_vial', position=Position(0, 0)))

@raises(RackPositionInvalid)
def test_rack_add_container_invalid_position():
    rack = Rack('gc_vial', 3, 4)
    # attempt to add a gc container to an invalid position
    rack.add_container(Container('gc_vial', position=Position(7, 0)))

def test_rack_remove_container():
    rack = Rack('gc_vial', 3, 4)
    # add a gc container
    container = Container('gc_vial', position=Position(0,0))
    rack.add_container(container)
    # remove the gc container
    rack.remove_container(container)

def test_rack_to_str():
    rack = Rack('gc_vial', 3, 4)
    rack_str = rack.to_str()
    assert isinstance(rack_str, str)
