import os
import requests
import json
import dotenv


def get_data():
    dotenv.load_dotenv()
    key = os.getenv('LICHESS_API_KEY')

    base = "https://explorer.lichess.org/lichess?"
    variant = "variant=standard"
    speed = "speeds=classical"
    rating = "ratings=2200"
    history = "history=false"

    url = base + "&".join([variant,speed,rating,history])

    data = requests.get(url,
        headers={"Authorization": key}
    )

    return data.json()


with open("data.json", "w") as file:
    data = get_data()
    json.dump(data, file)

# Vuosi
# elo
# avaus ECO
