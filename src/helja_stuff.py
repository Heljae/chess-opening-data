import os
import requests
# import json
from time import sleep
import dotenv
import pandas as pd


def get_data(year, speed, rating):
    vars = {
        "variant": "standard",
        "play": "",
        "speeds": f"{speed}",
        "ratings": f"{rating}",
        "since": f"{year}-01",
        # "until": f"{year}-12",
        "moves": "3"
    }

    return get_moves(vars)

    # url = base + "&".join([variant,speed,rating,since,until,moves])

    # if year == 2026:
    #     url = base + "&".join([variant,speed,rating,since,moves])
    # data = []
    
    # return data.json()

def get_moves(vars, move_count=0):
    dotenv.load_dotenv()
    key = os.getenv('LICHESS_API_KEY')
    base = "https://explorer.lichess.org/lichess?"

    if vars["play"] == "":
        url = base+"&".join([f"{key}={val}" for key, val in vars.items() if key != "play"])
    else:
        url = base+"&".join([f"{key}={val}" for key, val in vars.items()])

    while True:
        try:
            data = requests.get(url,
                headers={"Authorization": "Bearer "+key})
            data = data.json()
            break
        except:
            # print("not work, current position:", vars["play"])
            sleep(2)

    if move_count > 3:
        try: 
            if data["opening"]["name"]:
                opening = data["opening"]["name"]
            else:
                opening = vars["play"]
        except:
            opening = vars["play"]
        ans = ([vars["ratings"],
                vars["speeds"],
                vars["play"],
                opening,
                (data["white"]+data["black"]+data["draws"]),
                (data["white"],data["draws"],data["black"])])
        print(ans)
        return [ans]
    
    moves = []
    for move in data["moves"]:
        if vars["play"] != "":
            moves.append(",".join(vars["play"].split(",")+[move["uci"]]))
        else:
            moves.append(move["uci"])
    end_vars = []
    for move in moves:
        vars["play"] = move
        next_moves = get_moves(vars, move_count=move_count+1)
        for row in next_moves:
            if row not in end_vars and row != []:
                end_vars.append(row)
    return end_vars
    
def data_to_df(data):
    rating, time_control, moves, opening, amount, results = [], [], [], [], [], []
    for row in data:
        rating.append(row[0])
        time_control.append(row[1])
        moves.append(row[2])
        opening.append(row[3])
        amount.append(row[4])
        results.append(row[5])

    df = {
        "ratingClass": rating,
        "timeControl": time_control,
        "moves": moves,
        "opening": opening,
        "gameAmount": amount,
        "results": results
    }

    return pd.DataFrame(df)

# todo: normalization eli (pelien määrä tietyssä avauksessa / kaikkien pelien määrä samasta avauksesta)
def normalize_to_level():
    return


frames = []
for rating_class in ["0,1000", "1200,1400", "1600,2000", "2200,2500"]:
    for time in ["bullet", "blitz", "rapid", "classical"]:
        data = data_to_df(get_data(2021, time, rating_class))
        frames.append(data)

df = pd.concat(frames)
df.to_pickle('data_blitz.pkl')

data = pd.read_pickle("data_blitz.pkl")
with open("data.txt", "w") as file:
    file.write(data.to_string())
