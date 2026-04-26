from game.data import all_data as data
import random

place_types = [
    "square",
    "parc",
    "coffee",
    "bar",
    "casino",
    "restaurant",
    "cave",
    "shop"
]

class Place:

    def __init__(self):
        self.type = random.choice(place_types)
        self.name = random.choice(data()["place_prefix"]) + " " + self.type