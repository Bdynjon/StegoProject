import json


class Params:

    __slots__ = {
        "P",
        "block_size",
        "__rows",
        "channels",
        "hamming_block_size"
    }
    instance = None
    __default_parametrs_path = "data/params presets/default params.json"

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(Params, cls).__new__(cls)
        return cls.instance

    def __init__(self, path: str = None):
        path = path if path else self.__default_parametrs_path
        self.load_preset(path)

    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, value):
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError("'rows' must be a list with size 2")
        elif not (isinstance(value[0], int) and isinstance(value[1], int)):
            raise ValueError("'rows' must be a list of integers")
        elif not self.__check_rows_value(value):
            raise ValueError("values of rows can't be hihger the max value of rows in block")
        elif value[0] > value[1]:
            raise ValueError("first value must be lower than second in 'rows'")
        else:
            self.__rows = value

    def set_params(self, **kwargs):
        for key in sorted(kwargs):
            setattr(self, key, kwargs[key])

    def __check_rows(self):
        pass

    def calc_max_rows(self):
        return self.block_size*2 - 1

    def save_preset(self, path: str = None):
        path = path if path else self.__default_parametrs_path

        param_dict = {}
        for key in self.__slots__:
            key = key[2:] if key.startswith("__") else key
            param_dict[key] = getattr(self, key)

        with open(path, "w") as param_file:
            json.dump(param_dict, param_file, indent=2)

    def load_preset(self, path: str = None):
        path = path if path else self.__default_parametrs_path

        with open(path, "r") as param_file:
            param_dict = json.load(param_file)

        for key in param_dict:
            setattr(self, key, param_dict[key])

    def __check_rows_value(self, rows):
        max_row = self.block_size*2 - 1
        return rows[0] < max_row and rows[1] < max_row


def test():
    params = Params()
    print(params.P)

    params.set_params(channels={'blue': True,
                                'green': False,
                                'red': False})
    print(params.P)

    params.save_preset("params presets/my presets/test.json")
    params.load_preset("params presets/my presets/test.json")
    print(params.P)

    params1 = Params()
    print(params1.P)

    print(params)
    print(params1)


if __name__ == "__main__":
    test()
