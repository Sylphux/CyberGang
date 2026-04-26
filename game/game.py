import random

class Game:

    def __init__(self, cities):
        self.money = 100
        self.cities = cities
        print("Playing in city : " + self.cities[0].name)
        self.game_loop()

    def game_loop(self):
        while not is_game_over(self):
            input("Input: ")

# Game functions

def is_game_over(game):
    if game.money > 0:
        return False
    else:
        return True