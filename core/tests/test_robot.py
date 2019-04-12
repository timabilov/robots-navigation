import pytest

from core.bot import Robot, WrongRouteTargetException
from core.geo import Direction, Point
from core.route import RouteBuilder


class TestRobot:

    def test_create_robot(self):

        bot = Robot()
        assert bot.facing == Direction.NORTH
        assert bot.id is not None
        assert bot.group is None
        assert bot.position == Point(0, 0)

    def test_create_robot_group(self):
        bot = Robot(group='Stark')

        assert bot.group == 'Stark'

    @pytest.mark.parametrize("direction", (
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ))
    def test_robot_go(self, direction, robot):

        robot.go(direction=direction)

        assert robot.position.x == direction.x and robot.position.y == direction.y\
            , f'Robot position should be exactly same as {direction}: {direction.value}'

        robot.go(4)
        assert robot.position == direction * 5, 'Robot should go 5 blocks  total to North(default direction)'

    def test_robot_load(self, robot, routeb_north_factory):

        route = routeb_north_factory(3).build()

        robot.load(route)

        assert robot.position == Point(0, 3)

    def test_robot_different_instructions(self, robot):
        route = RouteBuilder().right().right().step(10).step(10, Direction.SOUTH).build()

        robot.load(route)
        assert robot.position == Point(0, -20)

        route = RouteBuilder().left().step(10).right().step(10, Direction.NORTH).build()

        robot.load(route)

        assert robot.position == Point(10, -10)

        route = RouteBuilder().step(100, Direction.NORTH).build()

        robot.load(route)
        assert robot.position == Point(10, 90)
        assert robot.facing == Direction.NORTH


    def test_incompatible_target(self, robot, routeb_north_factory):

        route = routeb_north_factory(2).target('Different').build()
        robot.group = 'Completely different'
        with pytest.raises(WrongRouteTargetException):
            robot.load(route)

    def test_compatible_target(self, robot, routeb_north_factory):
        route = routeb_north_factory(2).target('Same').build()

        robot.group = 'Same'
        robot.load(route)

    def test_route_start_intercept(self,robot, routeb_north_factory):

        route = routeb_north_factory(10).start(100, 200).build()

        robot.load(route)
        assert robot.position == Point(100, 210)


