#!/usr/bin/env python3
import requests, subprocess, shutil

standard_image = "/home/yulivee/.config/yulivee/favpic.jpg"
def main():
    output = subprocess.check_output("playerctl metadata | grep artUrl | awk '{print $3}'", shell=True)
    output = output.decode("utf-8")
    # print(output[:-1])


    player = subprocess.check_output("playerctl -l", shell=True)
    player = player.decode("utf-8")

    if player.split(".") == "brave":
            shutil.copyfile(standard_img, "scripts/album_cover.jpg")
    elif player == "cider":
        img_data = requests.get(output[:-1], stream=True).content
        with open(f'scripts/album_cover.jpg', 'wb') as handler:
            handler.write(img_data)

    print(output)

if __name__ == "__main__":
    main()
