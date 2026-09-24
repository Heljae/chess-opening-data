import os
import requests
import json
import dotenv
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Gets the data about played games and returns it in JSON
def get_data(year):
    dotenv.load_dotenv()
    key = os.getenv('LICHESS_API_KEY')

    base = "https://explorer.lichess.org/lichess?"
    variant = "variant=standard"
    speed = "speeds=classical"
    since = f"since={year}-01"
    until = f"until={year}-12"

    url = base + "&".join([variant,speed,since,until])

    data = requests.get(url,
        headers={"Authorization": "Bearer "+key})
    
    return data.json()


# Gets game data by year since this data is not included and stores it in a dataframe
#  TODO also include data about timecontrol. Also this is not optimal :(
years, ratings, games_played, openings = [], [], [], []
# There is much less data from years before 2015
# TODO normalization for number of games +other preprocessing
for year in range(2015, 2027):
    data = get_data(year)
    for move in data["moves"]:
        years.append(year)
        games_played.append(move["white"] + move["black"] + move["draws"])
        # Splitting ratings into "leagues" > do we want more or to adjust the classes?
        rating = move["averageRating"]
        if rating >= 1500:
            if rating >= 2000:
                if rating >= 2500:
                    rating = 2500
                else:
                    rating = 2000
            else:
                rating = 1500
        else:
            rating = 1000
        ratings.append(rating)
        openings.append(move["opening"]["eco"])

data_for_ml = {
    "year": years,
    "rating_class": ratings,
    "games_played": games_played,
    "opening":  openings
    }
df = pd.DataFrame(data_for_ml)

# Encoding the openining eco codes
enco = LabelEncoder()
df["opening_encoded"] = enco.fit_transform(df["opening"])
print(df)

# Pickle is much cooler than json B)
df.to_pickle('data_to_big_ml.pkl')