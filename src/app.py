import os
import requests
import json
import dotenv
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from time import sleep


# Gets the data about played games and returns it in JSON
def get_data(year, speed):
    dotenv.load_dotenv()
    key = os.getenv('LICHESS_API_KEY')

    base = "https://explorer.lichess.org/lichess?"
    variant = "variant=standard"
    speed = f"speeds={speed}"
    since = f"since={year}-01"
    until = f"until={year}-12"

    url = base + "&".join([variant,speed,since,until,"moves=20"])

    if year == 2026:
        url = base + "&".join([variant,speed,since,"moves=20"])

    data = requests.get(url,
        headers={"Authorization": "Bearer "+key})
    
    return data.json()

# Rating classes >1000, 1000-1200, 1200-1400 etc 
def rating_classes(rating):
    match rating:
        case r if r < 1200:
            return 1000
        case r if r in range(1200, 1400):
            return 1200
        case r if r in range(1400, 1600):
            return 1400
        case r if r in range(1600, 1800):
            return 1600
        case r if r in range(1800,2000):
            return 1800
        case r if r in range(2000, 2200):
            return 2000
        case r if r in range(2200, 2400):
            return 2200
        case r if r >= 2400:
            return 1000
        case _:
            return rating


# Gets game data by year since this data is not included and stores it in a dataframe
#  TODO also include data about timecontrol. Also this is not optimal :(
years, ratings, games_played, openings, timecontrol = [], [], [], [], []
# There is much less data from years before 2015
for year in range(2026, 2027):
    for time in ["bullet", "blitz", "rapid", "classical"]:
        sleep(1)
        try:
            data = get_data(year, time)
            print(year, time)
            all_games = data["white"]+data["draws"]+data["black"]
            if not data["moves"]:
                print("no moves")
                continue
            for move in data["moves"]:
                years.append(year)
                timecontrol.append(time)
                games_played.append((move["white"] + move["black"] + move["draws"])/all_games)
                rating = rating_classes(move["averageRating"])
                ratings.append(rating)
                openings.append(move["opening"]["name"])
        except:
            print("not working:", (year, time))

data_for_ml = {
    "year": years,
    "rating_class": ratings,
    "games_played": games_played,
    "opening":  openings,
    "timecontrol": timecontrol
    }
df = pd.DataFrame(data_for_ml)

# Encoding the openining eco codes
enco = LabelEncoder()
df["opening_encoded"] = enco.fit_transform(df["opening"])
df["timecontrol_encoded"] = enco.fit_transform(df["timecontrol"])
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)


# Pickle is much cooler than json B)
df.to_pickle('data_to_big_ml.pkl')