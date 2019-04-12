## timabilov / robots-navigation [![Build Status](https://travis-ci.com/timabilov/robots-navigation.svg?branch=master)](https://travis-ci.com/timabilov/robots-navigation)

# Robot API for navigation 

API Interface for scheduling robot routes.


Requirements:

 `Postgres 9.6`
```ini
Django==2.0.12
psycopg2==2.7.3.2
pyyaml==5.1
pytest==4.4.0
pytest-django==3.4.8
mixer==6.1.3
```


To just run script(down below) with already up & running Postgres :
```bash
(venv) $ ./script.sh
```


Or with docker-compose (Recommended):

```bash
$ docker-compose run --rm web ./script.sh
# or
$ docker-compose run --rm web  bash 
root@e2a026903899:/app# ./script.sh   
```

To run django project on docker-compose
```bash
./entry.sh
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

# We can use directly Robot API. Robots can be separated to groups for further relevant route consuming
r = Robot().forward(3).forward(5)

# Robot can interpret route which can be created by many different ways
# For incompatible routes `WrongRouteTargetException` may raise
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



* For millions of routes we should carefully optimize our database (indexes, consider partitioning). De-normalization. 
e.g. in that case de-normalizing of all other relations (Instruction) will be prioritized. Eventually we will have many indexed data everywhere for every purpose (Full text search-optimized, insert optimized and etc.) as table grows.  
* hundreds of instructions: For best performance De-normalize fields to plain binary value/string. But during that process we can maintain any index of this instructions wherever we want(Postgres, Elastic search  etc.)
   For 1-10 instructions, we can  store all this values on separate table if we want to get quick and flexible reports for example. 
* For many users: Server codebase should be thread-safe. Transaction Atomicity should be taken seriously. Redis cluster will be involved for tons of caching. Heavy profiling. Heavy writes will run on background(postgres as example). But indexes will be primary resource. Again, indexes.
* for frequently changed routes we should build flexible architecture, for example, where each route itself is some named instruction set/group. So we can use/store Route as instruction itself.
  Basically now we got modular, scalable solution for instructions. And this instruction set can be used by many other planners. Also we will get single source of truth(if we want). 
  