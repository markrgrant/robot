


class Container(object):
    """A Container has a specific type and can hold an object."""

    def __init__(self, container_type, contents=None, position=None,
                 barcode=None, destinations=None):
        self._contents = contents
        self._container_type = container_type
        self.position = position
        self.destinations = destinations

    def to_dict(self):
        return dict(
            contents=self._contents,
            container_type=self._container_type
        )

    def to_str(self):
        return "<t={0},p={1},c={2}".format(
            self._container_type,
            self.position,
            self._contents
        )

    def __str__(self):
        return self.to_str()

    def add_contents(self, contents):
        if self.is_empty is False:
            raise ContainerNotEmpty()
        self._contents = contents

    @property
    def contents(self):
        return self._contents

    def remove_contents(self):
        if self.is_empty is True:
            raise ContainerEmpty()
        contents = self._contents
        self._contents = None
        return contents

    def transfer(self, container):
        """
        Transfer the contents of the container into this container."""
        if self.is_empty is False:
            raise ContainerNotEmpty()
        self.add_contents(container.remove_contents())

    @property
    def container_type(self):
        return self._container_type

    @property
    def is_empty(self):
        return self._contents is None


class ContainerEmpty(Exception):
    pass

class ContainerNotEmpty(Exception):
    pass
