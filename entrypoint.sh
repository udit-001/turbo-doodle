#!/bin/bash

python tests.py || echo "Tests Failed!"
gunicorn --bind 0.0.0.0:5000 wsgi:app
