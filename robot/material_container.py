from container import (
    Container,
)



class MaterialContainer(Container):
    """
    A MaterialContainer is a type of Container that holds volumes
    of materials, subject to the following conditions:

    1. The total volume of all the materials in the container cannot
       exceed the maximum volume of the container.
    """

    def __init__(self, container_type, max_volume_in_ml, **kwargs):
        """
        """
        self.max_volume_in_ml = max_volume_in_ml
        super(MaterialContainer, self).__init__(container_type, **kwargs)

    def transfer(self, container, volume_in_ml):
        """
        Transfer all of the contents from the given container into
        this container.
        """
        contents = container.remove_contents(volume_in_ml)
        self.add_contents(**contents)

    @property
    def total_volume(self):
        """
        Returns the total volume in the container in mls.

        Returns:
            float: The total volume in the container in mls.
        """
        if self.contents is None:
            return 0.0
        return sum([v for k, v in self.contents.iteritems()])

    def add_contents(self, **contents):
        """
        Add the contents to this container.

        Args:
            contents (dict): a dictionary whose keys are material names and whose
                volumes are the volume of that material in mls being added.

        Returns:
            None

        Raises:
            NegativeVolume: if a volume provided is less than 0
            MaxVolumeExceeded: if the volume to be added would exceed the
                maximum volume of the container
        """
        volume_to_add = sum([v for k, v in contents.iteritems()])
        if self.total_volume + volume_to_add > self.max_volume_in_ml:
            raise MaxVolumeExceeded
        if self._contents is None:
            self._contents = {}
        for content_name, volume_in_ml in contents.iteritems():
            if volume_in_ml < 0:
                raise NegativeVolume()
            if content_name not in self._contents:
                self._contents[content_name] = volume_in_ml
            else:
                self._contents[content_name] += volume_in_ml

    def remove_contents(self, volume_in_ml):
        """remove the specified volume from each of the materials in
        the container.

        Returns:  a dictionary whose keys are the names of materials and whose
        values are all volume_in_ml.
        """
        removed_contents = dict()
        total_volume = 0
        if self._contents is None:
            raise NoContents()
        for k in self._contents:
            total_volume += self._contents[k]
        if volume_in_ml > total_volume:
            raise ContentVolumeExceeded()
        for content_name, content_volume in self._contents.items():
            volume_fraction = 1.0 - volume_in_ml/total_volume
            new_volume = self._contents[content_name] * volume_fraction
            if new_volume == 0:

                del self._contents[content_name]
            else:
                self._contents[content_name] = new_volume
            removed_contents[content_name] = content_volume  - new_volume
        return removed_contents

    def __repr__(self):
        return ("MaterialContainer(container_type='{0}', "
                "max_volume_in_ml={1})"
                ).format(
                    self.container_type, self.max_volume_in_ml
                )


class ContentNotFound(Exception):
    pass

class ContentVolumeExceeded(Exception):
    pass

class MaterialContainerMaxVolume(Exception):
    pass

class NoContents(Exception):
    pass

class NegativeVolume(Exception):
    pass

class MaxVolumeExceeded(Exception):
    pass
