import pytest

from core.bot import Instruction
from core.geo import Direction
from core.route import RouteBuilder, YamlRouteValidationException


class TestRouteBuilder:

    def test_route_builder_create(self):

        route_builder = RouteBuilder()
        assert route_builder.name is not None
        assert route_builder.instructions == []

    def test_route_step(self):
        route_builder = RouteBuilder()
        route_builder.step(10, Direction.EAST)

        assert len(route_builder.instructions) == 1
        assert route_builder.instructions[0] == f'{Instruction.EAST.value}:10'

    def test_route_forward_step(self):
        route_builder = RouteBuilder()
        route_builder.step(3)

        assert len(route_builder.instructions) == 1
        assert route_builder.instructions[0] == f'{Instruction.FORWARD.value}:3'

    def test_right(self):

        route_builder = RouteBuilder()
        route_builder.right()

        assert len(route_builder.instructions) == 1
        assert route_builder.instructions[0] == f'{Instruction.RIGHT.value}:'


    def test_many_instructions(self):

        route_builder = RouteBuilder()
        place = 'Where winter is coming'
        route_builder.step(10).right().left().reach(place)

        assert len(route_builder.instructions) == 4
        expected = [
            f'{Instruction.FORWARD.value}:10',
            f'{Instruction.RIGHT.value}:',
            f'{Instruction.LEFT.value}:',
            f'{Instruction.REACH.value}:{place}',
        ]
        assert route_builder.instructions == expected


    def test_build_route(self, routebuilder):

        route = routebuilder.build()

        assert route.name == routebuilder.name
        assert route.target == routebuilder._target
        assert route.start == routebuilder._start
        assert route.instructions == routebuilder.instructions



class TestYamlImport:

    def test_yaml_import(self, yaml_sample):

        routeset = RouteBuilder.from_yaml(yaml_sample)

        assert len(routeset.routes) == 2

        route1 = routeset.routes[0]
        assert route1.name == 'My route'
        assert route1.start == (10, 10)
        assert route1.instructions == [
            f'{Instruction.RIGHT.value}:',
            f'{Instruction.NORTH.value}:3',
            f'{Instruction.EAST.value}:3',
            f'{Instruction.RIGHT.value}:',
            f'{Instruction.FORWARD.value}:3',
            f'{Instruction.REACH.value}:Saint Valley',

        ]

        route2 = routeset.routes[1]
        assert route2.name == 'Route only for packagers'
        assert route2.target == 'Packagers'
        assert route2.instructions == [
            f'{Instruction.NORTH.value}:3',
            f'{Instruction.EAST.value}:3',
            f'{Instruction.RIGHT.value}:',
            f'{Instruction.FORWARD.value}:10',
        ]


    def test_wrong_yaml(self, yaml_wrong_sample):
        with pytest.raises(YamlRouteValidationException):
            routeset = RouteBuilder.from_yaml(yaml_wrong_sample)

