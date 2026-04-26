from game.game import Game
from game.characters import Character
from game.cities import City
from game.places import Place
import os

def main():
    os.system("clear")

    number_of_cities = 1
    number_of_characters_by_city = 100
    number_of_places_by_city = 20

    cities = []
    for i in range(number_of_cities):
        characters = []
        for i in range(number_of_characters_by_city):
            characters.append(Character())
        places = []
        for i in range(number_of_places_by_city):
            places.append(Place())
        for place in places:
            print(place.name)
        cities.append(City(places, characters))

    game = Game(cities)

main()