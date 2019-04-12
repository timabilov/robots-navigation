import enum


class Point:

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __add__(self, other):

        if isinstance(other, Vector):
            return self.__class__(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        return self

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Vector(Point):

    def __mul__(self, other):
        if isinstance(other, int):
            return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        if isinstance(other, int):
            self.x *= other
            self.y *= other
        return self


class Direction(Vector, enum.Enum):
    """
    Cardinal Direction. Fields sorted by natural "right turn" order
    """
    NORTH = 0, 1
    EAST = 1, 0
    SOUTH = 0, -1
    WEST = -1, 0

    def left(self) -> 'Direction':
        return self._relative_position(shift=-1)

    def right(self) -> 'Direction':
        return self._relative_position(shift=1)

    def _relative_position(self, shift: int) -> 'Direction':
        """
        Build relative state to make right turns.
        For that purpose we specially *ordered* direction values in declaration
        :param shift: positive means to right, left otherwise.
        :return Direction:
        """
        # Declaration already has natural ordering.
        ordered_direction = list(Direction)
        return ordered_direction[(ordered_direction.index(self) + shift) % 4]
