import json

def all_data():
    items = []
    with open("data/text_data.json") as json_file:
        items = json.load(json_file)
    return items