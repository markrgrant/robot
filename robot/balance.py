from container import Container


class Balance(Container):
    """
    A Balance Weighs a single container.  A Balance can weigh containers
    of any type.
    """
    _default_weight = 1.0

    def __init__(self):
        self._contents = None

    def to_dict(self):
        return dict(
            contents=self._contents
        )

    def add_container(self, container):
        if self._contents is not None:
            raise BalanceOccupied()
        self._contents = container

    def remove_container(self):
        if self._contents is None:
            raise BalanceEmpty()
        container = self._contents
        self._contents = None
        return container

    def is_empty(self):
        return self._contents is None

    def weigh_container(self):
        if self._contents is None:
            raise BalanceEmpty()
        return Balance._default_weight

    def to_str(self, indent=''):
        return indent + "Balance:\n\n{0}".format(
            self.container.to_str(indent + '  ') if self._contents
            else indent + '  ' + 'container=None'
        )



class BalanceOccupied(Exception):
    pass

class BalanceEmpty(Exception):
    pass
