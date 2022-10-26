import json


class Params:

    __slots__ = {
        "P",
        "rows",
        "__default_parametrs_path",
        "__is_loaded",
        "block_size",
        "channels",
        "hamming_block_size"
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Params, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__default_parametrs_path = "params presets/default params.json"
        self.load_preset()

    def set_params(self, P: int = None, rows: tuple = None, block_size: int = None, channels: dict = None,
                   hamming_block_size: int = None):
        self.P = P if P else self.P
        self.rows = rows if rows and (self.calc_max_rows() > rows[1]) else self.rows
        self.block_size = block_size if block_size else self.block_size
        self.channels = channels if channels else self.channels
        self.hamming_block_size = hamming_block_size if hamming_block_size else self.hamming_block_size

        self.save_preset()

    def __check_rows(self):
        pass

    def calc_max_rows(self):
        return self.block_size*2 - 1

    def save_preset(self, path: str = None):
        path = path if path else self.__default_parametrs_path

        param_dict = {
            "P": self.P,
            "rows": self.rows,
            "block_size": self.block_size,
            "channels": self.channels,
            "hamming_block_size": self.hamming_block_size
        }

        with open(path, "w") as param_file:
            json.dump(param_dict, param_file, indent=2)

    def load_preset(self, path: str = None):
        path = path if path else self.__default_parametrs_path

        with open(path, "r") as param_file:
            param_dict = json.load(param_file)

        for key in param_dict:
            setattr(self, key, param_dict[key])


if __name__ == "__main__":
    params = Params()
    print(params.P)

    params.set_params(channels={'blue':True,
                                'green':False,
                                'red':False})
    print(params.P)

    params.save_preset("params presets/my presets/test.json")
    params.load_preset("params presets/my presets/test.json")
    print(params.P)

    params1 = Params()
    print(params1.P)

    print(params)
    print(params1)