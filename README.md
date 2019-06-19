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

# or just with docker-compose (Recommended way)

$ docker-compose run --rm web ./script.sh
# or
$ docker-compose run --rm web  bash 
root@e2a026903899:/app# ./script.sh


```


To run django server with docker-compose:

```bash
# Docker compose
(venv) $ ./entry.sh
   
```

To run tests:
```bash
(venv) $ ./test.sh
# or
$ docker-compose run --rm web ./test.sh

```



 We can either use provided API:
 
```python
from core.bot import Robot
from core.geo import Direction
from core.route import RouteBuilder


route = RouteBuilder(name='Example route')\
    .start(245, 161)\
    .step(5, Direction.NORTH)\
    .right()\
    .reach('Statue of Old Man with Large Hat')\
    .step(25, Direction.WEST)\
    .left()\
    .step(3)\
    .build()
    
simple_robot = Robot()
# robot info will be logged
simple_robot.load(route)

print(f'Simple robot arrived: {simple_robot.position}')
```
Or import list of routes from yaml (custom defined - schema strict):
```yaml
# See: core.route_schema.SCHEMA
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

# Also robot can interpret route which can be created by many different ways
# Only if robot group does not comply to route target group(incompatible)
# - `WrongRouteTargetException` may raise
for i, route in enumerate(Route.objects.all(), start=1):
    print(f'Route: {i}')
    r.load(route)


print(f'Arrived: {r.position}')

# Route can be targeted to some dedicated robot group.
spawn_robots(3, group='Packagers')
route.notify(target='Packagers') # notify only 'Packagers' about this route

# we can notify all our robots about all our routes (groups also considered), to execute instructions.
routeset.notify_bots()




```


Logs for robot:

```
>> Robot:daf3fecb-19c0-44b7-aed0-af81ac315a20  <Example route> Position: (245, 161).
 - Instruction.NORTH: 5. Position: (245, 166)
 - Instruction.RIGHT: <>. Position: (245, 166)
 - Instruction.REACH: Statue of Old Man with Large Hat. Position: (245, 166)
 - Instruction.WEST: 25. Position: (220, 166)
 - Instruction.LEFT: <>. Position: (220, 166)
 - Instruction.FORWARD: 3. Position: (220, 163)
 * Robot:daf3fecb-19c0-44b7-aed0-af81ac315a20  completed. Position: (220, 163)

```



* For millions of routes we should carefully optimize our database (indexes, consider partitioning). De-normalization. 
e.g. in that case de-normalizing of all other relations (Instruction) will be prioritized. Eventually we will have many indexed data everywhere for every purpose (Full text search-optimized, insert optimized and etc.) as table grows.  
* hundreds of instructions: For best performance De-normalize fields to plain binary value/string. But during that process we can maintain any index of this instructions wherever we want(Postgres, Elastic search  etc.)
   For 1-10 instructions, we can  store all this values on separate table if we want to get quick and flexible reports for example. 
* For many users: Server codebase should be thread-safe. Transaction Atomicity should be taken seriously. Redis cluster will be involved for tons of caching. Heavy profiling. Heavy writes will run on background(postgres as example). But indexes will be primary resource. Again, indexes.
* for frequently changed routes we should build flexible architecture, for example, where each route itself is some named instruction set/group. So we can use/store Route as instruction itself.
  Basically now we got modular, scalable solution for instructions. And this instruction set can be used by many other planners. Also we will get single source of truth(if we want). 
