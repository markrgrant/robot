from container import Container


class Reader(Container):
    """
    A barcode reader.  Given a container, returns the barcode of that
    container, regardless of the type of the container.
    """

    def __init__(self):
        super(Reader, self).__init__('reader')

    def to_dict(self):
        return dict(
            contents=self._contents
        )

    def add_container(self, container):
        if self._contents is not None:
            raise ReaderOccupied()
        self._contents = container

    def remove_container(self):
        if self._contents is None:
            raise ReaderEmpty()
        container = self._contents
        self._contents = None
        return container

    def read_barcode(self):
        if self._contents is None:
            raise ReaderEmpty()
        if not hasattr(self._contents, 'barcode'):
            raise ReaderNoBarcode()
        return  self._contents.barcode

    @property
    def is_empty(self):
        return self._contents is None

    def to_str(self, indent=''):
        return indent + 'Reader:\n{0}'.format(
            self._contents.to_str(indent + '  ') if self._contents else '')


class ReaderOccupied(Exception):
    pass

class ReaderEmpty(Exception):
    pass


class ReaderNoBarcode(Exception):
    pass
