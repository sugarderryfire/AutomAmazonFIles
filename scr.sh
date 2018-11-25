#!/bin/bash

/usr/bin/Xvfb :99 -ac -screen 0 1024x768x8 & export DISPLAY=:99
python Automain.py bachelorette bachelorette.party.bachelor

