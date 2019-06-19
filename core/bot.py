import enum
import uuid

from core.geo import Direction, Point
from core.models import Route
from core.notifications import subscriber


@enum.unique
class Instruction(enum.Enum):
    """
    Simple instructions with flexible attached syntax for further parsing
    """
    LEFT = 'left'
    RIGHT = 'right'

    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'
    FORWARD = 'forward'

    REACH = 'reach'

    def is_direction(self):
        return self.name in Direction.__dict__.keys() or self.name == self.FORWARD

    def is_turn(self):
        return self.name in (self.LEFT, self.RIGHT)

# class City:
#
#     def __init__(self):


class WrongRouteTargetException(Exception):

    pass


@subscriber
class Robot:
    """
    Interface/API to give some orders. Default spawn direction: Direction.NORTH
    """
    def __init__(self, group=None):
        self.id = uuid.uuid4()
        self.group = group
        self.facing = Direction.NORTH
        self.position = Point(0, 0)

        self.route_ids = []

    def load(self, route: Route):
        """
        Load specific route information to execute immediately.
        :param route:
        :return:
        """
        # if route targeted for robot group
        if self.group and route.target and route.target != self.group:
            raise WrongRouteTargetException(
                f'{self}:{self.group} does not match to current route target "{route.name}"": {route.target}'
            )

        self.route_ids.append(route.id)
        if route.start:
            self.position = Point(route.start[0], route.start[1])

        print(f'>> {self}  <{route.name}> Position: {self.position}.')

        # Using appropriate bot API to handle all operations
        for instruction in route:
            directive, arg = instruction.split(':')
            command = Instruction(directive)

            if not arg:
                arg = None

            # execute
            getattr(self, command.value)(arg)

            print(f' - {command}: {arg or "<>"}. Position: {self.position}')
        print(f' * {self}  completed. Position: {self.position}')

    def go(self, blocks=1, direction=None):
        direction = self.facing if not direction else direction
        self.position += direction * int(blocks)
        self.facing = direction
        return self

    # Bot API

    def forward(self, blocks):
        return self.go(blocks, self.facing)

    def north(self, blocks):
        return self.go(blocks, direction=Direction.NORTH)

    def south(self, blocks):
        return self.go(blocks, direction=Direction.SOUTH)

    def east(self, blocks):
        return self.go(blocks, direction=Direction.EAST)

    def west(self, blocks):
        return self.go(blocks, direction=Direction.WEST)

    def left(self, times=1):
        if not times:
            times = 1
        for _ in range(times):
            self.facing = self.facing.left()
        return self

    def right(self,  times=1):
        if not times:
            times = 1
        for _ in range(times):
            self.facing = self.facing.right()
        return self

    def reach(self, destination):

        # if destination:
        #     print(f'  Heading to "{destination}"...')
        return self

    def __str__(self):
        return f'Robot:{self.id}'


def spawn_robots(count=10, group=None):

    return [Robot(group=group) for _ in range(count)]
