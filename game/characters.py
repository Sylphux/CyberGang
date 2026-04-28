from game.data import all_data as data
import random

weaknesses = [
    "bribing",
    "intimidation"
]
# rep is a reputation modifier
available_tags = [
    {"tag": "addict", "prob": 20, "rep": -5},
    {"tag": "dealer", "prob": 15, "rep": -10},
    {"tag": "cop", "prob": 15, "rep": -10},
    {"tag": "chemist", "prob": 10, "rep": -10},
    {"tag": "investigator", "prob": 7, "rep": 10},
    {"tag": "fixer", "prob": 8, "rep": 0},
    {"tag": "merchant", "prob": 8, "rep": 0},
    {"tag": "enforcer", "prob": 5, "rep": -20}
]

max_tags_per_char = 3

class Character:

    def __init__(self, name = "Driver"):
        self.name = random.choice(data()["first_names"]) + " " + random.choice(data()["last_names"])
        self.age = random.randrange(10, 25) + random.randrange(10, 25)
        self.loyalty = random.randrange(15, 85)
        self.toughness = random.randrange(30, 95)
        self.reputation = random.randrange(15, 85) - (50 - self.loyalty)
        self.money = random.randrange(50, 400)
        self.inv = []
        self.tags = []
        self.known_tags = []
        self.weakness = random.choice(weaknesses)
        for tag in available_tags:
            dice = random.randrange(1, 100)
            if dice <= tag["prob"] and not tag["tag"] in self.tags:
                self.tags.append(tag["tag"])
                self.reputation += tag["rep"]
        if self.reputation < 5:
            self.reputation = 5
        if self.reputation > 95:
            self.reputation = 95
        # if len(self.tags) > max_tags_per_char:
        #     for i in range(len(self.tags) - max_tags_per_char):
        #         self.tags.remove(random.choice(self.tags))
        if self.tags == []:
            self.tags = ["random"]
        # print("Char: " + self.name, "rep:", self.reputation, "loy:", self.loyalty)