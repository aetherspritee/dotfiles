eww_path="$PWD/"
winstate=$(eww windows -c "$eww_path" | grep lolpopup)

if [ "${winstate:0:1}" = "*" ]; then
    eww close lolpopup -c "$eww_path"
else
    eww open lolpopup -c "$eww_path"
fi
