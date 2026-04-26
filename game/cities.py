import random
from game.data import all_data as data

class City:

    def __init__(self, places, characters, random_city = True):
        self.name = random.choice(data()["city_names"])
        self.places = places
        self.characters = characters
