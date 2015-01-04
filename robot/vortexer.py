class Vortexer(object):
    """A Vortexer mixes the contents of specific kinds of Containers,
    subject to the following constraints:

    1. Only one container can be mixed at a time.

    2. The container's contents should be unmixed before mixing.

    3. The container must be of an appropriate type.
    """
    def __init__(self, container_types):
        """
        Args:
            container_types (list): A list of container type names that
            fit on the vortexer and can be vortexed.  Some container types,
            like bottles, shouldn't be vortexed.
        """
        self._contents = None
        self._container_types = container_types

    def to_dict(self):
        return dict(
            contents=self._contents
        )

    def add_container(self, container):
        if container.container_type not in self._container_types:
            raise VortexerInvalidContainerType()
        if self._contents is not None:
            raise VortexerOccupied()
        if container.is_mixed is True:
            raise VortexerContainerMixed()
        self._contents = container

    def vortex(self):
        if self._contents is None:
            raise VortexerEmpty()
        if self._contents.is_capped is False:
            raise VortexerContainerUncapped()
        self._contents.mix()

    def remove_container(self):
        if self._contents is None:
            raise VortexerEmpty()
        container = self._contents
        if container.is_mixed is False:
            raise VortexerContainerUnmixed()
        self._contents = None
        return container

    @property
    def is_empty(self):
        return self._contents is None

    def to_str(self):
        return self._to_str()

    def _to_str(self, indent=''):
        return indent + "Vortexer: {0}".format(
            self._contents.to_str(indent + '  ') if self._contents else '')


class VortexerOccupied(Exception):
    pass

class VortexerEmpty(Exception):
    pass

class VortexerContainerUncapped(Exception):
    pass

class VortexerContainerUnmixed(Exception):
    pass

class VortexerContainerMixed(Exception):
    pass

class VortexerInvalidContainerType(Exception):
    pass
