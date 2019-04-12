import os
import tempfile

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


@fixture
def routebuilder():
    route_builder = RouteBuilder()
    place = 'Where winter is coming'
    route_builder.step(10).right().left().reach(place)
    return route_builder


@fixture
def yaml_sample():
    content = """
                - name: 'My route'
                  start: '10:10'
                  steps:
                    - right:
                    - north: 3
                    - east: 3
                    - right:
                    - forward: 3
                    - reach: 'Saint Valley'

                - name: 'Route only for packagers'
                  target: "Packagers"
                  steps:
                    - north: 3
                    - east: 3
                    - right:

                    - forward: 10
            """

    new_file, filename = tempfile.mkstemp()

    os.write(new_file, content.encode())
    os.close(new_file)

    yield filename

    os.remove(filename)


@fixture
def yaml_wrong_sample():
    content = """
                - name: 'My route'
                  start: '10:10'
                  steps:
                    - iwantcakes:
                    
                - name: 'Route only for packagers'
                  wrong:
                  steps:
                    - north: 3
                    - east: 3
                    - right:
                    - forward: 10
            """

    new_file, filename = tempfile.mkstemp()

    os.write(new_file, content.encode())
    os.close(new_file)

    yield filename

    os.remove(filename)
