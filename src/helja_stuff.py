import app

ratings = [1000,1200,1400,1600,1800,2000,2200,2400]

def rating_classes(rating):
    match rating:
        case r if r in range(1200):
            return 1000
        case r if r in range(1200, 1400):
            return 1200
        case r if r in range(1400, 1600):
            return 1400
        case r if r in range(1600, 1800):
            return 1600
        case r if r in range(2000, 2200):
            return 2000
        case r if r in range(2200, 2400):
            return 2200
        case r if r > 2400:
            return 1000
        case _:
            return None

times = ["bullet", "blitz", "rapid", "classical"]

totals = []
for time in times:
    data = app.get_data(2025, time)
    total = data["white"]+data["draws"]+data["black"]
    moves = []

    total2 = 0
    for opening in data["moves"]:
        total2 += opening["white"]+opening["draws"]+opening["black"]

    totals.append((total, total2, len(data["moves"])))

[print(i) for i in totals]


