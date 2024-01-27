#!/bin/bash

bat=$(bt_bat)

if [ "$bat" == "" ]; then
    echo "No device connected"
else
    echo $bat
fi
