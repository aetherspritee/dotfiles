eww_path="$PWD/"
winstate=$(eww active-windows -c "$eww_path" | grep sysmenu)

if [ "${winstate:0:1}" = "s" ]; then
    eww close sysmenu -c "$eww_path"
else
    eww open sysmenu -c "$eww_path"
fi
