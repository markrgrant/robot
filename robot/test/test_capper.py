from ..capper import (
    Capper,
    CapperEmpty,
    CapperHasCap,
    CapperNoCap,
    CapperOccupied,
    CapperContainerCapped,
    CapperContainerUncapped
)
from nose.tools import raises
from ..vial import Vial


def test_init():
    capper = Capper(['gc_vial'])
    assert capper.is_empty is True
    assert capper.has_cap is False

def test_add_container():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    capper.add_container(container)
    assert capper.is_empty is False
    assert capper.has_cap is False

def test_remove_container():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    capper.add_container(container)
    assert capper.is_empty is False
    capper.remove_container()
    assert capper.is_empty is True
    assert capper.has_cap is False


@raises(CapperEmpty)
def test_remove_container_empty():
    capper = Capper(['gc_vial'])
    capper.remove_container()

def test_uncap():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    capper.add_container(container)
    capper.uncap()
    assert capper.has_cap
    assert container.is_capped is False

def test_cap():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    container._capped = False
    capper._has_cap = True
    capper.add_container(container)
    capper.cap()

@raises(CapperContainerUncapped)
def test_uncap_uncapped():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    container._capped = False
    capper.add_container(container)
    capper.uncap()


@raises(CapperContainerCapped)
def test_cap_capped():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    capper.add_container(container)
    capper.cap()

@raises(CapperHasCap)
def test_capper_has_cap():
    capper = Capper(['gc_vial'])
    capper._has_cap = True
    container = Vial(container_type='gc_vial')
    capper.add_container(container)
    capper.uncap()

@raises(CapperNoCap)
def test_capper_no_cap():
    capper = Capper(['gc_vial'])
    container = Vial(container_type='gc_vial')
    container._capped = False
    capper.add_container(container)
    capper._has_cap = False
    capper.cap()

@raises(CapperEmpty)
def test_cap_empty():
    capper = Capper(['gc_vial'])
    capper.cap()

@raises(CapperEmpty)
def test_uncap_empty():
    capper = Capper(['gc_vial'])
    capper.uncap()

@raises(CapperOccupied)
def test_load_container_occupied():
    capper = Capper(['gc_vial'])
    capper.add_container(Vial(container_type='gc_vial'))
    capper.add_container(Vial(container_type='gc_vial'))

def test_capper_to_str():
    capper = Capper(['gc_vial'])
    capper.to_str()
