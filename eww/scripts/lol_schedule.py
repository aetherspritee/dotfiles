import requests, re, calendar, json
from bs4 import BeautifulSoup
from pathlib import Path

home = str(Path.home())


months = list(calendar.month_name)
base_url = "https://liquipedia.net"
url = "https://liquipedia.net/leagueoflegends/api.php?"+"action=parse&format=json&page="+"Liquipedia:Matches"
headers = {
    'User-Agent': 'eww-bar-league-widget',
    'From': 'schautendustin@gmail.com',
    'Accept-Encoding': 'gzip'
}

team_regex = 'title="[a-z. A-Z0-9\']*"'
time_regex = "[A-Z][a-z]* [0-3]*[0-9], [0-9]{4} - [0-2]*[0-9]:[0-5][0-9]"
image_regex = "[a-z.A-Z%\/_0-9-\']*.png"

response = requests.get(url, headers=headers)
data = response.json()

text = data["parse"]["text"]["*"]

soup = BeautifulSoup(text)

left_teams = []
right_teams = []
times = []
left_images = []
right_images = []
tables = soup.findAll('table')

# print(tables[0])
for table in tables:
    if re.findall('"LCK"', str(table)) or re.findall('"LEC"',str(table)) or re.findall('"lpl"', str(table)):
        match_fillers = table.findAll('td', class_="match-filler")
        # print(match_fillers)
        for match_filler in match_fillers:
            print(match_filler)
            times.append(re.findall(time_regex,str(match_filler))[0])
        team1 = table.findAll('td', class_="team-left")
        # print(team1)
        for team in team1:
            left_teams.append(re.findall(team_regex,str(team))[0].split("=")[-1])
            left_images.append(base_url+re.findall(image_regex,str(team))[0])
        team2 = table.findAll('td', class_="team-right")
        # print(team2)
        for team in team2:
            right_teams.append(re.findall(team_regex,str(team))[0].split("=")[-1])
            right_images.append(base_url+re.findall(image_regex,str(team))[0])

games = []
formatted_time = []
for ts in times:
    parts = ts.split(" ")
    month = months.index(parts[0])
    day = parts[1][:-1]
    year = parts[2]
    time = parts[4].split(":")
    hour = str(int(time[0])+1)
    min = time[1]
    formatted_time.append([month, day, year, hour, min])

for t1,t2,t,i1,i2 in zip(left_teams,right_teams, formatted_time, left_images, right_images):
    print(f"{t1} vs {t2} at {t}")
    data = {"left_team": t1, "right_team": t2, "left_image": i1, "right_image": i2, "date": t}
    games.append(data)

games = {"games": games}

with open(home+"/.config/eww/scripts/games.json", "w") as f:
    pass
with open(home+"/.config/eww/scripts/games.json", "a") as f:
    json.dump(games, f)
