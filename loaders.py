import json


def load_key(path):
    with open(path, "r") as key_file:
        key_dict = json.load(key_file)

    return key_dict["seed"], key_dict["approp_blocks"]


def save_key(path, seed, approp_blocks):

    key_dict = {
        "seed": seed,
        "approp_blocks": approp_blocks
    }

    with open(path, "w") as key_file:
        json.dump(key_dict, key_file, indent=2)
