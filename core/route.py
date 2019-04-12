import uuid

import yaml
from cerberus import Validator

from core.bot import Instruction
from core.models import Route
from core.route_schema import SCHEMA


class YamlRouteValidationException(Exception):
    pass


class RouteSet:
    """
    Route Proxy for batch/bulk operations.
    """
    def __init__(self, routes):
        self.routes = routes

    def save(self):
        """
        Saves all routes in database
        :return:
        """
        Route.objects.bulk_create(self.routes)
        return self

    def notify_bots(self):
        """
        Notify all appropriate robots about all our routes
        :return:
        """
        for route in self.routes:
            route.notify()
        return self

    # ... any other operations such as bulk target set.


class RouteBuilder:
    """
    Fluent interface for creating route.
    """

    def __init__(self, name=None, start=None, target=None):
        self.name = name or uuid.uuid4()
        self._start = start
        self._target = target
        self.instructions = []

    @classmethod
    def from_yaml(cls, path):

        payload = yaml.safe_load(open(path, 'r'))
        routes = []
        v = Validator()
        if not v.validate({
            'root': payload
        }, SCHEMA):
            raise YamlRouteValidationException(v.errors)
        if isinstance(payload, dict):
            routes.append(RouteBuilder()._parse_route(payload))
        elif isinstance(payload, list):

            for item in payload:
                routes.append(RouteBuilder()._parse_route(item))

        return RouteSet([Route(
            name=builder.name,
            start=builder._start,
            target=builder._target,
            instructions=builder.instructions,
        ) for builder in routes])

    @classmethod
    def _parse_route(cls, payload):
        route = RouteBuilder()
        route.name = payload.get('name', uuid.uuid4())
        route._target = payload.get('target', None)
        if payload.get('start'):
            route._start = tuple(int(x) for x in payload.get('start').split(':'))

        for step in payload.get('steps'):
            directive, arg = list(step.items())[0]
            Instruction(directive)
            route.instructions.append(':'.join([directive, str(arg or '')]))
        return route

    def build(self):
        return Route(
            name=self.name,
            start=self._start,
            target=self._target,
            instructions=self.instructions,
        )

    def start(self, point_x, point_y):
        self._start = (point_x, point_y)
        return self

    def target(self, target):
        self._target = target
        return self

    def step(self, blocks, direction=None):

        instruction = getattr(Instruction, direction.name if direction else 'FORWARD')

        self.instructions.append(f'{instruction.value}:{blocks}')
        return self

    def left(self):
        self.instructions.append(Instruction.LEFT.value + ':')
        return self

    def right(self):
        self.instructions.append(Instruction.RIGHT.value + ':')
        return self

    def reach(self, destination):
        self.instructions.append(f'{Instruction.REACH.value}:{destination}')
        return self


