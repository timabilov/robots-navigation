## timabilov / robots-navigation [![Build Status](https://travis-ci.com/timabilov/robots-navigation.svg?branch=master)](https://travis-ci.com/timabilov/robots-navigation)

# Robot API for navigation 

To run project on docker-compose
```bash
./entry.sh
```


```ini
Django==2.0.12
psycopg2==2.7.3.2
pyyaml==5.1
pytest==4.4.0
pytest-django==3.4.8
mixer==6.1.3
```

```python
from core.geo import Direction
from core.route import RouteBuilder


# We can either use provided API

route = RouteBuilder(name='Example route')\
    .start(245, 161)\
    .step(5, Direction.NORTH)\
    .right()\
    .reach('Statue of Old Man with Large Hat')\
    .step(25, Direction.WEST)\
    .left()\
    .step(3)\
    .build()
```
Or read many routes from yaml:
```yaml
- name: 'My route'
  start: '10:10'
  steps:
    - north: 3
    - east: 3
    - right:
    - right:
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
```
```python
from core.bot import Robot, spawn_robots
from core.models import Route
from core.route import RouteBuilder

# Create routes from file and save all to database
routeset = RouteBuilder.from_yaml('route.yml').save()  # class RouteSet - wrapper

# Robot has own API. Also robots can be separated to groups for further relevant route consuming
r = Robot().forward(3).forward(5)

# Also robot can interpret route which can be created by many different ways
for i, route in enumerate(Route.objects.all(), start=1):
    print(f'Route: {i}')
    r.load(route)


print(f'Arrived: {r.position}')

# Route can be targeted to some dedicated robot group.
spawn_robots(3, group='Packagers')

# we can notify all our robots about all our routes (groups also considered), to execute instructions.
routeset.notify_bots()

# notify only 'New group' about this route
route.notify(target='New group')

```


Logs for robot:

```
>> Robot:1e3753ce-7d32-4733-ab6c-ce5cc1af82f0  <Route only for packagers> Position: (13, 16).
 - Instruction.NORTH: 3. Position: (13, 19)
 - Instruction.EAST: 3. Position: (16, 19)
 - Instruction.RIGHT: <>. Position: (16, 19)
 - Instruction.FORWARD: 10. Position: (16, 9)
 * Robot:1e3753ce-7d32-4733-ab6c-ce5cc1af82f0  completed. Position: (16, 9)

```