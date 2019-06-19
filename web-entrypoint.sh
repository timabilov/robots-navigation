#!/usr/bin/env bash

./manage.py migrate --no-input
exec "$@"
