from pytest import fixture

from core.bot import Robot
from core.geo import Direction
from core.route import RouteBuilder


@fixture
def robot():
    bot = Robot()
    return bot


@fixture
def route(routebuilder):

    return routebuilder.build()


@fixture
def routeb_north_factory():

    return lambda blocks: RouteBuilder().step(blocks, Direction.NORTH)
