eww_path="$PWD/"
winstate=$(eww active-windows -c "$eww_path" | grep calendar)

if [ "${winstate:0:1}" = "c" ]; then
    eww close calendar -c "$eww_path"
else
    eww open calendar -c "$eww_path"
fi
