#!/bin/bash

dropbox &
emacs --daemon &
source venv/bin/activate && python ".config/eww/scripts/lol_schedule.py"
