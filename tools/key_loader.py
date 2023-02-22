import json


class Key:

    __slots__ = {
        "__seed",
        "__default_key_path"
    }

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Seed value must be positive integer")
        else:
            self.__seed = value

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Key, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__default_key_path = "../data/keys/default key.json"

    def load_key(self, path: str = None):
        path = path if path else self.__default_key_path

        with open(path, "r") as key_file:
            key_dict = json.load(key_file)

        for key in key_dict:
            setattr(self, key, key_dict[key])

    def save_key(self, path: str = None):
        path = path if path else self.__default_key_path

        key_dict = {
            "seed": self.seed
        }

        with open(path, "w") as key_file:
            json.dump(key_dict, key_file, indent=2)


def test():
    key = Key()
    key.seed = 20
    print(key.seed)
    key.save_key()
    key.load_key()
    print(key.seed)


if __name__ == "__main__":
    test()

