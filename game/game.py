import random

class Game:

    def __init__(self, cities):
        self.money = 100
        self.cities = cities
        get_game_info(self) # Prints all that is in the game recursively
        self.game_loop()

    def game_loop(self):
        while not is_game_over(self):
            input("\nYou: ")

# Game functions

def is_game_over(game):
    if game.money > 0:
        return False
    else:
        return True

def get_game_info(game):
    print("--- Game info ---\n")
    for city in game.cities:
        print("City: " + city.name)
        print("  Places:")
        for place in city.places:
            print("    " + place.name)
        print("  Characters:")
        for char in city.characters:
            print("    " + char.name + ", age: " + str(char.age))
    print("-----------------")