#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

keybLayout=$(setxkbmap -v | awk -F "+" '/symbols/ {print $2}')

if [ $keybLayout = "be" ]; then
  run sxhkd -c ~/.config/bspwm/sxhkd/sxhkdrc-azerty &
else
  run sxhkd -c ~/.config/bspwm/sxhkd/sxhkdrc &
fi

feh --bg-fill ~/Wallpapers/gruvbox_girl_dark.png

export ZDOTDIR=$HOME/.config/zsh
dex $HOME/.config/autostart/arcolinux-welcome-app.desktop
xsetroot -cursor_name left_ptr &

run nm-applet &
run pamac-tray &
run xfce4-power-manager &
numlockx on &
blueberry-tray &
picom --config $HOME/.config/picom/picom.conf &
run dropbox &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
run volumeicon &
run dropbox &
run dunst &
emacs --daemon &

setxkbmap -option caps:escape

# bash ~/.config/polybar/launch.sh --blocks
# bash ~/.config/polybar/blocks/launch.sh
eww open bar0
bash wmname LG3D
playerctld daemon
run dropbox &
run dunst &

pkill double_border; ~/.config/bspwm/scripts/double_border &
source venv/bin/activate && python "~/.config/eww/scripts/lol_schedule.py"
