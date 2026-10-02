import app

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

data = app.get_data()
