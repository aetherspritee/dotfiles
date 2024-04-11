eww_path="$PWD/"
winstate=$(eww active-windows | grep lolpopup)

if [ "${winstate:0:1}" = "l" ]; then
    eww close lolpopup -c "$eww_path"
else
    eww open lolpopup -c "$eww_path"
fi
