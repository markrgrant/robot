from position import Position


class Rack(object):
    """
    A Rack is a rectangular grid that stores Containers of the same type.

    Items in the grid are referenced by their (x, y) coordinates, starting
    from (0, 0) and ending with (width-1, height-1).
    """

    def __init__(self, container_type, width, height):
        """Create a rack for storing containers of the specified type,
        with the given width and height.

        Args:
            container_type (string): The type of container to be stored
            width (int): The width of the rack
            height (int): The height of the rack

        Returns:
            Rack: a new empty Rack with the given width and height
        """
        self._container_type = container_type
        self._containers = [
            [None for h in xrange(height)] for w in xrange(width)
        ]
        self._width = width
        self._height = height

    def to_dict(self):
        data = dict(
            container_type=self._container_type,
            width=self._width,
            height=self._height
        )
        containers = []
        for row in self._containers:
            row_dict = []
            for cont in row:
                if cont is None:
                    row_dict.append(dict(contents=dict(empty=None)))
                else:
                    row_dict.append(cont.to_dict())
            containers.append(row_dict)
        data['containers'] = containers
        return data


    def get_position(self, index):
        """
        A helper method for converting an an index into an x-y position
        """
        x = index / self._height;
        y = index - x * self._height;
        return Position(x=x, y=y)

    def add_container(self, container):
        """
        Add the container to this rack

        Args:
            container (Container): the container to be added
            position (Position): The position in the rack to add the container

        Returns:
            None

        Raises:
            RackContainerTypeInvalid
            RackPositionOccupied
            RackPositionInvalid
        """
        position = container.position
        self._validate_position(position)
        if container._container_type != self._container_type:
            raise RackContainerTypeInvalid()
        if self._containers[position.x][position.y] is not None:
            raise RackPositionOccupied()
        self._containers[position.x][position.y] = container

    def remove_container(self, container):
        """
        Remove and return the Container at the given position.

        Args:
            position (Position): the position of the Container to be returned.

        Returns:
            Container: the container that was at the given position.

        Raises:
            RackContainerNotFound
            RackPositionInvalid
        """
        position = container.position
        self._validate_position(position)
        found_container = self._containers[position.x][position.y]
        if found_container is None:
            raise RackContainerNotFound()
        if container != found_container:
            raise DuplicateRackPosition()
        self._containers[position.x][position.y] = None
        return container

    def _validate_position(self, position):
        """
        Verifies that the given Position object is within the bounds of the
        rack.

        Args:
            position (Position): The position to be tested for validity

        Returns:
            None

        Raises:
            RackPositionInvalid
        """
        if (position.x < 0 or position.x >= self._width or position.y < 0
                or position.y >= self._height):
            raise RackPositionInvalid()

    def to_str(self, indent=''):
        """
        Return a string representation of the Rack and its contents.
        """
        contents = '\n'
        for row in self._containers:
            contents += indent + '  '
            for obj in row:
                contents += obj.to_str() + ' ' if obj else '0'
            contents += "\n"
        return indent + "Rack: container_type=" + self._container_type + \
            "\n" + contents + "\n"


class RackPositionOccupied(Exception):
    pass

class RackPositionInvalid(Exception):
    pass

class RackContainerTypeInvalid(Exception):
    pass

class IndexTooLarge(Exception):
    pass

class RackContainerNotFound(Exception):
    pass

class DuplicateRackPosition(Exception):
    pass
