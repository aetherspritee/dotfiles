#!/usr/bin/env python3
import json, datetime, argparse, requests
from string import Formatter
from datetime import timedelta

def strfdelta(tdelta, fmt='{D:02}d {H:02}h {M:02}m', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """

    # Convert tdelta to integer seconds.
    if inputtype == 'timedelta':
        remainder = int(tdelta.total_seconds())
    elif inputtype in ['s', 'seconds']:
        remainder = int(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = int(tdelta)*60
    elif inputtype in ['h', 'hours']:
        remainder = int(tdelta)*3600
    elif inputtype in ['d', 'days']:
        remainder = int(tdelta)*86400
    elif inputtype in ['w', 'weeks']:
        remainder = int(tdelta)*604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('W', 'D', 'H', 'M', 'S')
    constants = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--team1", help="get team one")
    parser.add_argument("--logo1", help="get team one logo", type=int, choices=[0,1,2,3,4,5,6])
    parser.add_argument("--team2", help="get team two")
    parser.add_argument("--logo2", help="get team two logo", type=int, choices=[0,1,2,3,4,5,6])
    parser.add_argument("--time", help="get team two",type=int, choices=[0,1,2,3,4,5,6])
    args = parser.parse_args()

    with open("scripts/games.json", "r") as f:
        data = json.load(f)["games"]


    now = datetime.datetime.now()
    upcoming_matches = []
    live_match = []
    for game in data:
        raw_date = game["date"]
        raw_date = f"{raw_date[0]}-{raw_date[1]}-{raw_date[2]} {raw_date[3]}:{raw_date[4]}"
        datetime_object = datetime.datetime.strptime(raw_date, '%m-%d-%Y %H:%M')
        diff = datetime_object-now
        game["diff"] = diff.total_seconds()
        game["diff2"] = diff
        if diff.total_seconds() > 0:
            if len(upcoming_matches) == 0:
                upcoming_matches.append(game)
            else:
                index = 0
                for i in range(len(upcoming_matches)):
                    if upcoming_matches[i]["diff"] < game["diff"]:
                        index = i
                        break

                # Inserting n in the list
                if index == len(upcoming_matches):
                    upcoming_matches = upcoming_matches[:index] + [game]
                else:
                    upcoming_matches = upcoming_matches[:index] + [game] + upcoming_matches[index:]

        else:
            if len(live_match) == 0:
                live_match = [game]
            # check if theres a live game
            if diff.total_seconds() >= live_match[0]["diff"]:
                live_match = [game]

                if abs(diff.total_seconds()) < 2*60*60:
                    # print(abs(diff.total_seconds()))
                    live_match[0]["diff2"] = "LIVE!"

    upcoming_matches = upcoming_matches[::-1]
    # print(f"{upcoming_matches = }")
    if len(live_match) == 0:
        pass
    elif abs(live_match[0]["diff"]) < 2*60*60:
        upcoming_matches = live_match+upcoming_matches
    # print(live_match)
    # print(upcoming_matches)

    if args.team1:
        print(upcoming_matches[0]["left_team"])

    if args.logo1:
        url = upcoming_matches[args.logo1-1]["left_image"]
        img_data = requests.get(url).content
        with open(f'scripts/logoA{args.logo1-1}.png', 'wb') as handler:
            handler.write(img_data)
        print(f"scripts/logoA{args.logo1-1}.png")

    if args.team2:
        print(upcoming_matches[0]["right_team"])

    if args.logo2:
        url = upcoming_matches[args.logo2-1]["right_image"]
        img_data = requests.get(url).content
        with open(f'scripts/logoB{args.logo2-1}.png', 'wb') as handler:
            handler.write(img_data)
        print(f"scripts/logoB{args.logo2-1}.png")

    if args.time:
        if upcoming_matches[args.time-1]["diff2"] != "LIVE!":
            print(f" in {strfdelta(upcoming_matches[args.time-1]['diff2'])}")
        else:
            print("LIVE!")
if __name__ == "__main__":
    main()
