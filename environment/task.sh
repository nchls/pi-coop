#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/home/pi/.local/lib/python3.7/site-packages/:/home/pi/coop/
export DJANGO_SETTINGS_MODULE='coop.settings'
/usr/bin/python3 /home/pi/coop/environment/tasks.py
