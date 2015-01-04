from ..barcoded import (
    Barcoded,
    BarcodeImmutable
)
from nose.tools import raises


def test_barcoded():
    b1 = Barcoded()
    b2 = Barcoded()
    assert b1.barcode != b2.barcode


@raises(BarcodeImmutable)
def test_barcoded_set_raises():
    b = Barcoded()
    b.barcode = 'different_barcode'

