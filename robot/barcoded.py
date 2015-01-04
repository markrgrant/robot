def _barcode_generator():
    barcode = 1
    while True:
        yield barcode
        barcode = barcode + 1

_barcode_iterator = _barcode_generator()


class Barcoded(object):
    """
    A mixin to be used on objects that are barcoded.  Note that the
    barcode is automatically assigned when the object is created via
    a singleton barcode generator.
    """
    def __init__(self, *args, **kwargs):
        self._barcode = next(_barcode_iterator)
        super(Barcoded, self).__init__(*args, **kwargs)

    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, barcode):
        raise BarcodeImmutable()


class BarcodeImmutable(Exception):
    pass
