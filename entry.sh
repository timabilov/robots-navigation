#!/usr/bin/env bash

docker-compose run --rm web ./manage.py migrate --no-input
docker-compose up