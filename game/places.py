from game.data import all_data as data
import random

place_types = [
    "place",
    "parc",
    "coffee",
    "subway",
    "bar",
    "casino",
    "restaurant",
    "shop"
]

class Place:

    def __init__(self):
        self.type = random.choice(place_types)
        self.name = random.choice(data()["place_prefix"]) + " " + self.type
        # self.boss = "unknown_boss"
        self.size = random.randrange(1, 3)
        self.cookable = False
        self.reputation = random.randrange(25, 75) # the badder the reputation, the more risk to cops
        self.expenses = 0
        self.light = random.randrange(10, 90) # allows to deal secretly
        if not is_public(self):
            self.expenses = random.randrange(50, 150)
            self.cookable = True
        self.pop = []
        self.max_pop = round((self.size * 10) / 2)

def is_public(p):
    if p.type == "place" or p.type == "parc" or p.type == "subway":
        return True
    return False