#!/bin/bash

run dropbox &
emacs --daemon &
source venv/bin/activate && python ".config/eww/scripts/lol_schedule.py"
