from ..capped import (
    Capped,
    AlreadyCapped,
    AlreadyUncapped
)
from nose.tools import raises


def test_capped():
    capped_object = Capped()
    assert capped_object.is_capped is True
    capped_object.uncap()
    assert capped_object.is_capped is False

@raises(AlreadyCapped)
def test_already_capped():
    c = Capped()
    c.cap()

@raises(AlreadyUncapped)
def test_already_uncapped():
    c = Capped()
    c.uncap()
    c.uncap()
