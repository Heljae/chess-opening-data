import os
import requests
import json
from time import sleep
import dotenv
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from time import sleep


# Gets the data about played games and returns it in JSON
def get_data(year, speed, rating):
    dotenv.load_dotenv()
    key = os.getenv('LICHESS_API_KEY')

    base = "https://explorer.lichess.org/lichess?"
    variant = "variant=standard"
    speed = f"speeds={speed}"
    rating = f"ratings={rating}"
    since = f"since={year}-01"
    until = f"until={year}-12"

    url = base + "&".join([variant,speed,rating,since,until,"moves=20"])

    if year == 2026:
        url = base + "&".join([variant,speed,rating,since,"moves=20"])

    data = requests.get(url,
        headers={"Authorization": "Bearer "+key})
    
    return data.json()

# Gets game data by year and timecontrol usingget_data since this data is not otherwise included in fetched data
# Encodes fields that need to be encoded and stores this data in a pickle
# 5 loops is the looptedoop trifecta
def data_by_year_and_timecontrol():
    years, ratings, games_played, openings, timecontrol = [], [], [], [], []
    # There is very little data from before 2015
    for year in range(2015, 2027):
        # We do not care about correspondance or ultrabullet. The former is oldschool and later bullshit
        for time in ["bullet", "blitz", "rapid", "classical"]:
            for rating_class in ["0,1000", "1200,1400", "1600,2000", "2200,2500"]:
                while True:
                    try:
                        print(year, rating_class, time)
                        data = get_data(year, time, rating_class)
                        all_games = data["white"]+data["draws"]+data["black"]
                        for move in data["moves"]:
                            years.append(year)
                            timecontrol.append(time)
                            games_played.append((move["white"] + move["black"] + move["draws"])/all_games)
                            ratings.append(rating_class)
                            openings.append(move["opening"]["name"])
                        break
                    except:
                        # Need to sleep or we get error
                        print("woompwoomp")
                        sleep(3)

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
    df["rating_class_encoded"] = enco.fit_transform(df["rating_class"])

    df = df.drop('opening', axis=1)
    df = df.drop('timecontrol', axis=1)
    df = df.drop('rating_class', axis=1)

    print(df)

    # Pickle is much cooler than json B)
    df.to_pickle('data_to_big_ml.pkl')

data_by_year_and_timecontrol()