import json


class Key:

    __slots__ = {
        "seed",
        "approp_blocks",
        "__default_key_path"
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Key, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__default_key_path = "keys/default key.json"
        self.load_key()

    def load_key(self, path: str = None):
        path = path if path else self.__default_key_path

        with open(path, "r") as key_file:
            key_dict = json.load(key_file)

        for key in key_dict:
            setattr(self, key, key_dict[key])

    def save_key(self, path: str = None):
        path = path if path else self.__default_key_path

        key_dict = {
            "seed": self.seed,
            "approp_blocks": self.approp_blocks
        }

        with open(path, "w") as key_file:
            json.dump(key_dict, key_file, indent=2)


if __name__ == "__main__":
    key = Key()
    key.seed = 20
    key.save_key()
    key.load_key()
    print(key.seed)

