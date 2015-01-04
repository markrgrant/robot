from ..material_container import (
    MaterialContainer,
    NegativeVolume,
    MaxVolumeExceeded
)
from nose.tools import raises


def test_init():
    c = MaterialContainer('test', max_volume_in_ml=1.5)
    assert c.is_empty is True

def test_add_contents():
    c = MaterialContainer('test', max_volume_in_ml=20.0)
    c.add_contents(water=1.0)
    c.add_contents(water=2.0)
    c.add_contents(ethanol=1.0)
    result = c.remove_contents(1.0)
    assert result['water'] == .750
    assert result['ethanol'] == .250

def test_remove_contents():
    c = MaterialContainer('test', max_volume_in_ml=1.5)
    c.add_contents(water=1.0)
    contents = c.remove_contents(0.5)
    assert contents['water'] == 0.5
    remainder = c.remove_contents(0.5)
    assert remainder['water'] == 0.5

def test_transfer():
    c_from = MaterialContainer('test', max_volume_in_ml=1.5)
    c_to = MaterialContainer('test', max_volume_in_ml=1.5)
    c_from.add_contents(water=1.0)
    c_to.transfer(c_from, 0.5)
    contents = c_to.remove_contents(0.5)
    assert contents['water'] == 0.5

def test_is_empty():
    c = MaterialContainer('test', max_volume_in_ml=1.5)
    assert c.is_empty is True
    c.add_contents(water=1.0)
    assert c.is_empty is False

def test_repr():
    c = MaterialContainer('test', max_volume_in_ml=1.5)
    c.add_contents(water=1.0)
    print c

@raises(NegativeVolume)
def test_raises_invalid_volume():
    c = MaterialContainer('test', max_volume_in_ml=1.5)
    c.add_contents(water=-1.0)
    c.to_str()

@raises(MaxVolumeExceeded)
def test_raises_max_volume_exceeded():
    c = MaterialContainer('test', max_volume_in_ml=2.0)
    c.add_contents(water=3.0)
