import random
import os
import datetime

max_actions = 3

class Game:

    def game_loop(self):
        while not is_game_over(self):
            # MORNING BACKEND PHASE
            self.day += 1
            people_go_to_places(self)
            # CHOICES PHASE
            print_title("Day " + str(self.day) + " | Ready for business.", 1)
            for i in range(max_actions):
                print_title(("What will you do ? " + str(i + 1) + "/" + str(max_actions)), 2)
                choose_main_action(self)
            # MARKET PHASE
                # harvest created drugs
                # distribute drugs to your dealers
                # Buy places

    def __init__(self, cities):
        self.money = 200
        self.pending_infos : []
        self.pending_actions: []
        self.day = 0
        self.cities = cities
        self.inv = []
        self.city = cities[0] # Sets the active city
        self.friends = [] # pour les relations avec les autres personnages
        self.known_places = []
        self.owned_places = []
        self.prison = [] # Where found criminals are locked in
        self.current_place = "Home"
        ### RANDOM SEEDING ###
        for i in range(3):
            self.friends.append(self.city.characters[random.randrange(0, len(self.city.characters))])
        for i in range(3):
            self.known_places.append(self.city.places[random.randrange(0, len(self.city.places))])
        ### START GAME HERE ###
        # print_title("Starting game...", p=1)
        self.game_loop()

##################################
# Game functions
##################################

def choose_main_action(game):
    macro_actions = {
        "meet": "Meet a friend somewhere (" + str(len(game.friends)) + " known.)",
        "explore": "Explore the city to discover new places (" + str(len(game.city.places) - len(game.known_places)) + " remaining.)",
        "goto": "Go to a specific place you know (" + str(len(game.known_places)) + " known.)",
    }
    possible_actions = []
    if game.friends != []:
        possible_actions.append("meet")
    if len(game.known_places) < len(game.city.places):
        possible_actions.append("explore")
    if game.known_places != []:
        possible_actions.append("goto")
    print()
    for i, action in enumerate(possible_actions):
        print("  [" + str(i) + "] " + macro_actions[action])
    selected_action = possible_actions[ask_for_n(possible_actions)]
    if selected_action == "meet":
        meet_a_friend(game)
    if selected_action == "explore":
        explore(game)
    if selected_action == "goto":
        goto(game)

def goto(game):
    place = select_a_place(game)
    visit_place(place)
    place_actions(game, place)

def explore(game):
    print("\nWandering around the city, you discover a new place.")
    undiscovered = []
    for place in game.city.places:
        if not place in game.known_places:
            undiscovered.append(place)
    place = random.choice(undiscovered)
    game.known_places.append(place)
    visit_place(place)
    place_actions(game, place)

def place_actions(game, place):
    game.current_place = place
    if place.pop != []:
        interact(game, place, place.pop[ask_for_n(place.pop, "Interact: ")])
    else:
        print("\nThere is nothing to do here. You leave the place.")
    game.current_place = "Home"

def ask_for_n(arr, choice_text="Your choice: "):
    ask = ""
    while True:
        ask = input("\n" + choice_text)
        if ask.isdigit() and int(ask) < len(arr):
            return int(ask)
        if ask == "":
            random_option = random.randrange(0, len(arr))
            print("System: Randomly chose option [" + str(random_option) + "]")
            return random.randrange(0, len(arr))
        print("Wrong input. Please input a valid digit.")

def list_arr(arr):
    s = ""
    for item in arr:
        s = s, item
    return s

def short_friend_description(char):
    s = ""
    if char.known_tags != []:
        s += list_arr(char.known_tags)
    if s != "":
        return "(" + s + ")"
    else:
        return ""

def select_a_place(game):
    print()
    for i, place in enumerate(game.known_places):
        print("  [" + str(i) + "] " + place.name + " (" + describe_place(place, short=True) + ")")
    selected_place = game.known_places[ask_for_n(game.known_places)]
    return selected_place

        
def meet_a_friend(game):
    print("\nWho do you wanna meet?")
    print()
    for i, char in enumerate(game.friends):
        print("  [" + str(i) + "] " + char.name, short_friend_description(char))
    selected_friend = game.friends[ask_for_n(game.friends)]
    print("\nWhere ?")
    selected_place = select_a_place(game)
    print("\nYou chose to meet " + selected_friend.name + " in " + selected_place.name + ".")
    for p in game.city.places:
        if selected_friend in p.pop:
            p.pop.remove(selected_friend)
    selected_place.pop.append(selected_friend)
    visit_place(selected_place)
    interact(game, selected_place, selected_friend)

def interact(game, place, char):
    print("\nYou interact with " + char.name + ".")

def people_go_to_places(game):
    characters = game.city.characters
    places = game.city.places
    rep_tolerance = 20
    random.shuffle(characters)
    for char in characters:
        random.shuffle(places)
        for place in places:
            if place.reputation in range((char.reputation - rep_tolerance), (char.reputation + rep_tolerance)):
                if len(place.pop) < place.max_pop:
                    place.pop.append(char)
                    # print(char.name, char.reputation, "went to " + place.name, place.reputation)
                    break
                    
def describe_place(place, short=False):
    light_text = ""
    # Light
    if place.light < 20:
        light_text = "very dark"
    elif place.light < 40:
        light_text = "a bit dark"
    elif place.light < 60:
        light_text = "well lit"
    elif place.light < 80:
        light_text = "bright"
    elif place.light < 80:
        light_text = "very bright"
    elif place.light >= 80:
        light_text = "filled with light"
    # Size
    size_text = ""
    match place.size:
        case 1:
            size_text = "small"
        case 2:
            size_text = "spacious"
        case 3: 
            size_text = "big"
    # Reputation
    reputation_text = ""
    if place.reputation < 20:
        reputation_text = "smells bad and people are shady"
    elif place.reputation < 40:
        reputation_text = "is not very welcoming"
    elif place.reputation < 60:
        reputation_text = "seems normal"
    elif place.reputation < 101:
        reputation_text = "has good vibes"

    if short == False:
        return "\nThis " + place.type + " is " + size_text + " and " + light_text + ". It " + reputation_text + "."
    elif short == True:
        return size_text.capitalize() + " and " + light_text + ", " + reputation_text + "."

def visit_place(place, debug=False):
    print_title(place.name)
    print(describe_place(place))
    if place.pop == []:
        print("There is no one here today.")
    else:
        print("Some people are here :")
        print()
        for i, char in enumerate(place.pop):
            char_vibes = ""
            if char.reputation < 40:
                char_vibes = ", has bad vibes."
            else:
                char_vibes = ", has good vibes."
            print(" [" + str(i) +"] " + char.name, str(char.age) + char_vibes)
    
    if debug == True:
        print_title("DEBUG PLACE")
        print_instance(place)
        for char in place.pop:
            print("---")
            print_instance(char, 2)

def print_title(text = "unknown_title", p=3):
    char = "="
    match p:
        case 3:
            char = "-"
        case 2:
            char = "="
        case 1:
            char = "⁝"
    title_len = 30
    side_spaces = round((title_len - len(text))/2)
    print("\n" + char * title_len)
    print(" " * side_spaces + text + " " * side_spaces)
    print(char * title_len)

def is_game_over(game):
    if game.money > 0:
        return False
    else:
        return True

def get_game_info(game):
    print_title("Game info")
    for city in game.cities:
        print("City: " + city.name)
        print("  Places:")
        for place in city.places:
            print("    " + place.name)
            print_instance(place, 5)
        print("  Characters:")
        for char in city.characters:
            print("    " + char.name)
            print_instance(char, 5)
        print("  Friends:")
        for char in game.friends:
            print("    " + char.name)
            print_instance(char, 5)
        print("  Discovered places:")
        for pl in game.known_places:
            print("    " + pl.name)
            print_instance(pl, 5)
    print("-----------------")

def print_instance(i, tabs = 0):
    for key, value in vars(i).items():
                print(" " * tabs + key +  ": " + str(value))