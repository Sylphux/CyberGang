import json

color_dict = {
    "BLACK": "0;30m",
    "RED": "0;31m",
    "GREEN": "0;32m",
    "BROWN": "0;33m",
    "BLUE": "0;34m",
    "PURPLE": "0;35m",
    "CYAN": "0;36m",
    "LIGHT_GRAY": "0;37m",
    "DARK_GRAY": "1;30m",
    "LIGHT_RED": "1;31m",
    "LIGHT_GREEN": "1;32m",
    "YELLOW": "1;33m",
    "LIGHT_BLUE": "1;34m",
    "LIGHT_PURPLE": "1;35m",
    "LIGHT_CYAN": "1;36m",
    "LIGHT_WHITE": "1;37m",
    "BOLD": "1m",
    "FAINT": "2m",
    "ITALIC": "3m",
    "UNDERLINE": "4m",
    "BLINK": "5m",
    "NEGATIVE": "7m",
    "CROSSED": "9m",
    "END": "0m",
    "COLOR_END": "0m"
}

class ANSI():

    def stylize(string, style):
        code = color_dict[style.upper()]
        return "\33[" + code.format(code=code) + string + "\33[" + color_dict["COLOR_END"].format(code=code)

def all_data():
    items = []
    with open("data/text_data.json") as json_file:
        items = json.load(json_file)
    return items