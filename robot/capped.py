class Capped(object):
    """
    A mixin to be used with objects that are capped.
    """

    def __init__(self, *args, **kwargs):
        self._capped = True
        super(Capped, self).__init__(*args, **kwargs)

    def cap(self):
        if self.is_capped is True:
            raise AlreadyCapped()
        self._capped = True

    def uncap(self):
        if self.is_capped is False:
            raise AlreadyUncapped()
        self._capped = False

    @property
    def is_capped(self):
        return self._capped


class AlreadyCapped(Exception):
    pass


class AlreadyUncapped(Exception):
    pass
