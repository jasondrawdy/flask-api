#!/bin/sh

# Make sure that we're in the correct working directory for running the API.
cd src

# Calling main is done only for testing and we should be using docker-compose
# to actually start this script, the container, and services; including Nginx.
python3 main.py #! USE A REAL WSGI SERVER FOR FLASK LIKE GUNICORN (EXAMPLE BELOW)!
# gunicorn main:'create_service()' -w 4 --threads 2 -b 0.0.0.0:80