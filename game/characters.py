from game.data import all_data as data
import random

class Character:

    def __init__(self, name = "Driver"):
        self.name = random.choice(data()["first_names"]) + " " + random.choice(data()["last_names"])
        self.age = random.randrange(10, 25) + random.randrange(10, 25)