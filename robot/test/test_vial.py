from ..vial import (
    Vial,
    VialCapped,
    VialUncapped,
    VialUnmixed
)
from nose.tools import raises


def test_init():
    v = Vial('gc_vial')
    assert v.is_capped is True
    assert v.is_mixed is False
    assert v.container_type == 'gc_vial'
    assert v.is_empty is True

def test_mix():
    v = Vial('gc_vial')
    assert v.is_mixed is False
    v.mix()
    assert v.is_mixed is True

def test_uncap():
    v = Vial('gc_vial')
    assert v.is_capped is True
    v.uncap()
    assert v.is_capped is False

def test_cap():
    v = Vial('gc_vial')
    v.uncap()
    assert v.is_capped is False
    v.cap()
    assert v.is_capped is True

def test_remove_contents():
    v = Vial('gc_vial')
    v.add_contents(water=1.0)
    contents = v.remove_contents(1.0)
    assert contents['water'] == 1.0

def test_str():
    vial = Vial('gc_vial')
    vial_str = vial.to_str()
    assert isinstance(vial_str, str)

@raises(VialUnmixed)
def test_remove_unmixed():
    v = Vial('gc_vial')
    v.add_contents(water=1.0)
    v.add_contents(ethanol=1.0)
    v.remove_contents(1.0)

@raises(VialUncapped)
def test_uncap_uncapped_error():
    v = Vial('gc_vial')
    assert v.is_capped is True
    v.uncap()
    v.uncap()

@raises(VialCapped)
def test_cap_capped_error():
    v = Vial('gc_vial')
    assert v.is_capped is True
    v.cap()


