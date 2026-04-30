import random
import os
import datetime
import math
from game.utils import all_data as data
from game.utils import ANSI

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
                print_inv_simple(self, self)
                print_title(
                    ("What will you do ? " + str(i + 1) + "/" + str(max_actions)), 2
                )
                choose_main_action(self)
            # MARKET PHASE
            # harvest created drugs
            # distribute drugs to your dealers
            # Buy places
            # EXPENSES
            self.money -= calculate_expenses(self)
        death_recap(self)

    def __init__(self, cities):
        self.name = "Player"
        self.money = 200
        self.pending_infos = []
        self.pending_actions = []
        self.day = 0
        self.cities = cities
        self.inv = data()["starter_inv"]
        self.city = cities[0]
        self.friends = []
        self.known_places = []
        self.owned_places = []
        self.prison = []  # Where found criminals are locked in
        self.current_place = "Home"
        self.home_rent = 35
        for i in range(3):
            self.friends.append(
                self.city.characters[random.randrange(0, len(self.city.characters))]
            )
        for i in range(3):
            self.known_places.append(
                self.city.places[random.randrange(0, len(self.city.places))]
            )
        ### START GAME HERE ###
        self.game_loop()


##################################
# CORE FUNCTIONS
##################################

def choose_main_action(game):
    macro_actions = {
        "meet": "Meet a friend somewhere (" + str(len(game.friends)) + " known.)",
        "bail_out": "Bail a friend out of prison",
        "explore": "Explore the city to discover new places ("
        + str(len(game.city.places) - len(game.known_places))
        + " remaining.)",
        "goto": "Go to a specific place you know ("
        + str(len(game.known_places))
        + " known.)",
    }
    possible_actions = []
    if game.friends != []:
        possible_actions.append("meet")
        for friend in game.friends:
            if friend in game.prison:
                possible_actions.append("bail_out")
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
    if selected_action == "bail_out":
        print("To implement...")

###############################
# VISUALS, UTILS & MESSAGES
###############################

def list_arr(arr):
    s = ""
    for item in arr:
        s = s, item
    return s

def print_inv_simple(game, person, money=True, inv=True):
    print_title(person.name + " 's inventory", 3)
    print()
    if inv:
        longest_lines = {
            "name": 0,
            "type": 0,
            "description": 0,
            "q": 0,
            "price": 0,
        }
        for item in person.inv:
            for key, value in item.items():
                length = len(str(value))
                if length > longest_lines[key]:
                    longest_lines[key] = length
        # Columns titles
        line_to_print = []
        for key, value in longest_lines.items():
            spaces = longest_lines[key] - len(key)
            line_to_print.append(key.upper() + "_" * spaces)
        print("_|_".join(line_to_print))
        # Item lines
        for item in person.inv:
            line_to_print = []
            for (
                key,
                value,
            ) in item.items():
                if key == "price":
                    value = (str(value) + " (" + str(value * item["q"]) + ")")
                spaces = longest_lines[key] - len(str(value))
                line_to_print.append(str(value) + " " * spaces)
            print(" | ".join(line_to_print))
    # Money
    if money:
        print()
        expenses = game.home_rent
        if person == game:
            for place in game.owned_places:
                expenses += place.expenses
        account = [
            {"money": str(person.money)},
            {"expenses": str(expenses)},
            {"remaining days": str(math.floor(person.money / expenses))}
        ]
        # Define the longest lines
        longest_lines = {}
        for item in account:
            for key, value in item.items():
                longest_lines[key] = 0
        for item in account:
            for key, value in item.items():
                length = 0
                if len(key) > len(value):
                    length = len(key)
                else:
                    length = len(value)
                if length > longest_lines[key]:
                    longest_lines[key] = length
        # Columns titles
        line_to_print = []
        for key, value in longest_lines.items():
            spaces = longest_lines[key] - len(key)
            line_to_print.append(key.upper() + "_" * spaces)
        print("_|_".join(line_to_print))
        # Item lines
        line_to_print = []
        for item in account:
            for (
                key,
                value,
            ) in item.items():
                spaces = longest_lines[key] - len(str(value))
                line_to_print.append(str(value) + " " * spaces)
        print(" | ".join(line_to_print))

def transfer_item(game, sender, recipient, item, q):
    remove_item(game, sender, q, item)
    add_item(game, recipient, q, item)

def transfer_money(game, sender, recipient, q):
    sender.money -= q
    recipient.money += q

def is_a_friend(game, char):
    if char in game.friends:
        return True
    return False

def print_title(text="unknown_title", p=3):
    char = "="
    match p:
        case 3:
            char = "-"
        case 2:
            char = "="
        case 1:
            char = "⁝"
    title_len = 50
    side_spaces = round((title_len - len(text)) / 2)
    print("\n" + char * title_len)
    print(ANSI.stylize(" " * side_spaces + text + " " * side_spaces, "red"))
    print(char * title_len)

def print_instance(i, tabs=0):
    for key, value in vars(i).items():
        print(" " * tabs + key + ": " + str(value))

def death_recap(game):
    print("\nAfter " + str(game.day) + " days, you lost.")
    print(
        "You discovered "
        + str(round(len(game.known_places) / len(game.city.places)) * 100)
        + " percent of the city."
    )
    print("You made friends with " + str(len(game.friends)) + " people.")
    secrets_n = 0
    for friend in game.friends:
        for disco in friend.known_tags:
            secrets_n += 1
    print(
    "You were able to discover " + str(secrets_n) + " secrets about your friends. Congrats."
    )
    print(
        "\nThere are some things you regret, other that puts you under shame. But there's one thing that made you very proud. You made a lot of money. ("
        + str(game.money)
        + "$)"
    )
    print("Dont worry too much. Everyone goes some day. Today was just your time.\n")

###############################
# PLACES
###############################

def goto(game):
    place = select_a_place(game)
    visit_place(game, place)
    place_actions(game, place)

def place_actions(game, place):
    game.current_place = place
    if place.pop != []:
        interact(game, place, place.pop[ask_for_n(place.pop, "Interact: ")])
    else:
        print("\nThere is nothing to do here. You leave the place.")
    game.current_place = "Home"

def explore(game):
    print("\nWandering around the city, you discover a new place.")
    undiscovered = []
    for place in game.city.places:
        if not place in game.known_places:
            undiscovered.append(place)
    place = random.choice(undiscovered)
    game.known_places.append(place)
    visit_place(game, place)
    place_actions(game, place)

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
        return (
            "\nThis "
            + place.type
            + " is "
            + size_text
            + " and "
            + light_text
            + ". It "
            + reputation_text
            + "."
        )
    elif short == True:
        return (
            size_text.capitalize() + " and " + light_text + ", " + reputation_text + "."
        )

def visit_place(game, place, debug=False):
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
            print(
                " [" + str(i) + "] " + char.name + ", " + str(char.age) + char_vibes,
                get_char_appearence(game, char),
            )
    if debug == True:
        print_title("DEBUG PLACE")
        print_instance(place)
        for char in place.pop:
            print("---")
            print_instance(char, 2)

###############################
# CHARACTERS
###############################

def short_friend_description(char):
    s = ""
    if char.known_tags != []:
        s = (", ").join(char.known_tags)
    if s != "":
        return "(" + s + ")"
    else:
        return ""

def meet_a_friend(game):
    print("\nWho do you wanna meet?")
    print()
    for i, char in enumerate(game.friends):
        print("  [" + str(i) + "] " + char.name, short_friend_description(char))
    selected_friend = game.friends[ask_for_n(game.friends)]
    print("\nWhere ?")
    selected_place = select_a_place(game)
    print(
        "\nYou chose to meet "
        + selected_friend.name
        + " in "
        + selected_place.name
        + "."
    )
    for p in game.city.places:
        if selected_friend in p.pop:
            p.pop.remove(selected_friend)
    selected_place.pop.append(selected_friend)
    visit_place(game, selected_place)
    interact(game, selected_place, selected_friend)


def interact(game, place, char):
    print("\nYou interact with " + char.name + ".")
    interact_actions = {
        "chat": "Chat and get to know him/her better",
        "sell": "Sell drugs",
        "buy": "Buy items (drugs, weapons, other items)",
        "kill": "Kill this person (with poison, a weapon, by hand...)",
        'indimidate': "Intimidate this person to state who's the boss.",
        "bribe": "Buy this persons fidelity with money"
    }
    possible_actions = []
    possible_actions.append("chat")
    for item in game.inv:
        if item["name"] == "drugs":
            possible_actions.append("sell")
            break
    print()
    for i, action in enumerate(possible_actions):
        print("  [" + str(i) + "] " + interact_actions[possible_actions[i]])
    selected_action = possible_actions[ask_for_n(possible_actions)]
    print()
    match selected_action:
        case "chat":
            print("You chose to chat with " + char.name + ".")
            chances_to_reveal = 0 + 100 - char.toughness
            dice = random.randrange(1, 101)
            if dice < chances_to_reveal and len(char.known_tags) < len(char.tags):
                discoverable = []
                for tag in char.tags:
                    if not tag in char.known_tags:
                        discoverable.append(tag)
                discovered = random.choice(discoverable)
                char.known_tags.append(discovered)
                print("You discovered that " + char.name + " is a " + discovered)
                befriend(game, char)
            else:
                print(
                    "You did not discover anything interesting about " + char.name + "."
                )
        case "sell":
            print("You try to sell " + char.name + " drugs.")
            chances_to_sell = random.randrange(0, 10)
            max_q = 3
            if is_a_friend(game, char):
                chances_to_sell += 10 + round(char.loyalty / 7)
            if "random" in char.tags:
                chances_to_sell += 20
                max_q = 3
            if "addict" in char.tags:
                chances_to_sell += 60
                max_q = 8
            if "dealer" in char.tags:
                chances_to_sell += 70
                max_q = 20
            if "cop" in char.tags:
                chances_to_sell -= 40
            if "merchant" in char.tags:
                chances_to_sell += 20
                max_q = 20
            if random.randrange(1, 101) < chances_to_sell:
                available_q = 0
                drugs_price = 10
                drug_item = {}
                for item in game.inv:
                    if item["name"] == "drugs":
                        available_q = item["q"]
                        drugs_price = item["price"]
                        drug_item = item
                can_buy_q = math.floor(char.money / drugs_price)
                if can_buy_q > available_q:
                    can_buy_q = available_q
                if can_buy_q > max_q:
                    can_buy_q = max_q
                if can_buy_q < 1:
                    print(char.name + " would like to buy, but is too poor.")
                else:
                    print(
                        char.name
                        + " agreed to buy "
                        + str(can_buy_q)
                        + "g of drugs from you for "
                        + str(can_buy_q * drugs_price)
                        + "$."
                    )
                    transfer_item(game, game, char, drug_item, can_buy_q)
                    transfer_money(game, char, game, can_buy_q * drugs_price)
                    cop_watches(game, place, char, crime_level=1)
            else:
                print(char.name + " wasn't interested.")
                # if "cop" in char.tags:
                if "cop" in char.tags:
                    instant_game_over(game, "You tried to sell drugs to a cop.")

def befriend(game, char):
    if not char in game.friends:
        print("\n" + char.name + " became your friend.")
        char.loyalty += 10
        game.friends.append(char)

def people_go_to_places(game):
    characters = game.city.characters
    places = game.city.places
    rep_tolerance = 20 # Repartition modifier
    random.shuffle(characters)
    for place in game.city.places:
        place.pop = []
    for char in characters:
        random.shuffle(places)
        for place in places:
            if place.reputation in range(
                (char.reputation - rep_tolerance), (char.reputation + rep_tolerance)
            ):
                if len(place.pop) < place.max_pop:
                    place.pop.append(char)
                    break

def get_char_appearence(game, char):
    total_city_pop = len(game.city.characters)
    medium_richness = 0
    for i_char in game.city.characters:
        medium_richness += i_char.money
    medium_richness /= total_city_pop
    medium_richness = round(medium_richness)
    if char.money < medium_richness / 2:
        return "Looks poor."
    if char.money < medium_richness:
        return "Is clothed normally."
    if char.money < medium_richness * 2:
        return "Looks priviledged."
    else:
        return "Looks rich."

###############################
# TESTS
###############################

def is_game_over(game):
    for action in game.pending_actions:
        if action["action"] == "arrested":
            print_title("GAME OVER - You were arrested while sleeping.", 1)
            return True
    if game.money > 0:
        return False
    else:
        print_title("GAME OVER - You lost all your money.", 1)
        return True

###############################
# MISC EVENTS & ACTIONS
###############################

def select_a_place(game):
    print()
    for i, place in enumerate(game.known_places):
        print(
            "  ["
            + str(i)
            + "] "
            + place.name
            + " ("
            + describe_place(place, short=True)
            + ")"
        )
    selected_place = game.known_places[ask_for_n(game.known_places)]
    return selected_place

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

def cop_watches(game, place, char, crime_level):
    cop_presence = False
    for guy in place.pop:
        if "cop" in guy.tags:
            print("\nYou feel observed.")
            cop_presence = True
            break
    if cop_presence:
        risk_factor = random.randrange(0, 10) + (place.light / 2)
        if random.randrange(0, 101) < risk_factor:
            suspicion = random.randrange(0, 101)
            if suspicion < (crime_level * 10) * 2:
                instant_game_over(game, "A cop saw you deal and locked you in.")
            else:
                print("Cops are launching an investigation on you.")

def add_item(game, recipient, q, trade_item):
    for item in recipient.inv:
        if item["name"] == trade_item["name"]:
            item["q"] += q
            return
    new_item = dict(trade_item)
    new_item["q"] = q
    recipient.inv.append(new_item)


def remove_item(game, recipient, q, trade_item):
    for item in recipient.inv:
        if item["name"] == trade_item["name"]:
            item["q"] -= q
            if item["q"] < 1:
                recipient.inv.remove(item)

def instant_game_over(game, reason):
    print_title("GAME OVER - " + reason, 1)
    death_recap(game)
    quit()

def calculate_expenses(game):
    expenses = game.home_rent
    for place in game.owned_places:
        expenses += place.expenses
    return expenses