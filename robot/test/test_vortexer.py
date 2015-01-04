from ..vortexer import (
    Vortexer,
    VortexerEmpty,
    VortexerOccupied,
    VortexerContainerUncapped,
    VortexerContainerUnmixed,
    VortexerContainerMixed,
    VortexerInvalidContainerType
)
from ..vial import Vial
from nose.tools import raises

valid_container_types = ['gc_vial']
invalid_container_type = 'bottle'

def test_init():
    vortexer = Vortexer(valid_container_types)
    assert vortexer._contents is None

def test_add_container():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    vortexer.add_container(container)
    assert vortexer._contents == container

def test_remove_container():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    vortexer.add_container(container)
    assert vortexer._contents == container
    vortexer.vortex()
    removed_container = vortexer.remove_container()
    assert container == removed_container
    assert vortexer._contents is None
    assert vortexer.is_empty

@raises(VortexerContainerUnmixed)
def test_remove_container_unmixed():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    vortexer.add_container(container)
    vortexer.remove_container()

@raises(VortexerContainerMixed)
def test_add_container_mixed():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    container.mix()
    vortexer.add_container(container)

def test_mix():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    vortexer.add_container(container)
    vortexer.vortex()
    container = vortexer.remove_container()
    assert container.is_mixed

@raises(VortexerContainerUncapped)
def test_mix_uncapped():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    container._capped = False
    vortexer.add_container(container)
    vortexer.vortex()

@raises(VortexerOccupied)
def test_read_occupied():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type='gc_vial')
    vortexer.add_container(container)
    vortexer.add_container(container)

@raises(VortexerEmpty)
def test_read_empty():
    vortexer = Vortexer(valid_container_types)
    vortexer.vortex()

@raises(VortexerEmpty)
def test_remove_empty():
    vortexer = Vortexer(valid_container_types)
    vortexer.remove_container()

def test_to_str():
    vortexer = Vortexer(valid_container_types)
    vortexer.to_str()

@raises(VortexerInvalidContainerType)
def test_invalid_container_type():
    vortexer = Vortexer(valid_container_types)
    container = Vial(container_type=invalid_container_type)
    vortexer.add_container(container)
