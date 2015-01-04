

class Capper(object):
    """
    A capper is responsible for capping and uncapping containers, subject
    to certain restrictions:

    1. A capper can only contain one container at a time.
    2. A capper can only cap/decap containers of a certain type.
    3. A capper can only recap the same container that it uncapped.
    """
    def __init__(self, container_types):
        """
        Args:
            container_types (list): A list of container types that the
            capper can cap/uncap
        """
        self._container_types = container_types
        self._contents = None  # The container being held
        self._has_cap = False  # the capper is not currently holding a cap
        self._cap_container = None

    def to_dict(self):
        return dict(
            has_cap=self._has_cap,
            contents=self._contents
        )

    def add_container(self, container):
        if self._contents is not None:
            raise CapperOccupied()
        if container.container_type not in self._container_types:
            raise CapperContainerType()
        self._contents = container

    def remove_container(self):
        if self._contents is None:
            raise CapperEmpty()
        container = self._contents
        self._contents = None
        return container

    def uncap(self):
        if self._contents is None:
            raise CapperEmpty()
        if self._contents._capped is False:
            raise CapperContainerUncapped()
        if self._has_cap:
            raise CapperHasCap()
        self._contents.uncap()
        self._has_cap = True

    def cap(self):
        if self._contents is None:
            raise CapperEmpty()
        if self._contents._capped:
            raise CapperContainerCapped()
        if self.has_cap is False:
            raise CapperNoCap()
        self._contents.cap()
        self._has_cap = False

    @property
    def is_empty(self):
        return self._contents is None

    @property
    def has_cap(self):
        return self._has_cap is True

    def to_str(self, indent=''):
        return indent + "Capper:\n\n{0}".format(
            self._contents.to_str(indent + '  ') if self._contents else \
            indent  + '  ' + 'container=None')


class CapperContainerUncapped(Exception):
    """cannot uncap an uncapped container"""
    pass


class CapperContainerType(Exception):
    """The capper doesn't support the given container type"""
    pass

class CapperContainerCapped(Exception):
    """cannot cap a capped container"""
    pass

class CapperHasCap(Exception):
    """capper already has a cap and cannot uncap another container"""
    pass

class CapperNoCap(Exception):
    """capper has no cap and cannot cap the container"""
    pass

class CapperEmpty(Exception):
    """
    a container cannot be removed from the capper because it has no
    container
    """
    pass

class CapperOccupied(Exception):
    """
    A container cannot be added to the capper because it contains a
    container already
    """
    pass
