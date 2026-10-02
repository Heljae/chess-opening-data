import os
import requests
import json
import dotenv
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Gets the data about played games and returns it in JSON
def get_data(year, speed):
    dotenv.load_dotenv()
    key = os.getenv('LICHESS_API_KEY')

    base = "https://explorer.lichess.org/lichess?"
    variant = "variant=standard"
    speed = f"speeds={speed}"
    since = f"since={year}-01"
    until = f"until={year}-12"

    url = base + "&".join([variant,speed,since,until])

    data = requests.get(url,
        headers={"Authorization": "Bearer "+key})
    
    return data.json()

# Rating classes >1000, 1000-1200, 1200-1400 etc 
def rating_classes(rating):
    if rating >= 1400:
        if rating >= 1600:
            if rating >= 1800:
                if rating >= 2000:
                    if rating >= 2400:
                        rating = 2400
                    else:
                        rating = 2000
                else:
                    rating = 1800       
            else:
                rating = 1600
        else:
            rating = 1400
    elif rating >= 1200:
        rating = 1200
    else:
        rating = 1000
    return rating


# Gets game data by year since this data is not included and stores it in a dataframe
#  TODO also include data about timecontrol. Also this is not optimal :(
years, ratings, games_played, openings, timecontrol = [], [], [], [], []
# There is much less data from years before 2015
for year in range(2015, 2027):
    for time in ["bullet", "blitz", "rapid", "classical"]:
        data = get_data(year, time)
        print(data)
        all_games = data["white"]+data["draws"]+data["black"]
        for move in data["moves"]:
            years.append(year)
            timecontrol.append(time)
            games_played.append((move["white"] + move["black"] + move["draws"])/all_games)
            rating = rating_classes(move["averageRating"])
            ratings.append(rating)
            openings.append(move["opening"]["name"])

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
print(df)

# Pickle is much cooler than json B)
df.to_pickle('data_to_big_ml.pkl')