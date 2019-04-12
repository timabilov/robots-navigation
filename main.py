import os

import yaml

from core.route import RouteBuilder


builder = None
try:
    builder = RouteBuilder.from_yaml('route.yml')
except yaml.YAMLError as exc:

    if hasattr(exc, 'problem_mark'):
        mark = exc.problem_mark

        print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
    print('Cannot parse file')
    os._exit(1)


builder