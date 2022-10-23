import json


class Params:

    __slots__ = {
        "P",
        "HF",
        "LF",
        "Pl",
        "Ph",
        "rows",
        "__default_parametrs_path",
        "__is_loaded",
        "block_size"
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Params, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__default_parametrs_path = "params presets/default params.json"
        self.load_preset()

    def set_params(self, P=None, HF=None, LF=None, Pl=None, Ph=None, rows=None, block_size=None):
        self.P = P if P else self.P
        self.HF = HF if HF else self.HF
        self.LF = LF if LF else self.LF
        self.Pl = Pl if Pl else self.Pl
        self.Ph = Ph if Ph else self.Ph
        self.rows = rows if rows else self.rows
        self.block_size = block_size if block_size else self.block_size

        self.save_preset()

    def save_preset(self, path: str = None):
        path = path if path else self.__default_parametrs_path

        param_dict = {
            "P": self.P,
            "HF": self.HF,
            "LF": self.LF,
            "Pl": self.Pl,
            "Ph": self.Ph,
            "rows": self.rows,
            "block_size": self.block_size
        }

        #if path != self.__default_parametrs_path:
        #    directory_path, save_file = path.rsplit("/", 1)
        #    directory = pathlib.Path(directory_path)

        #    for file in directory.iterdir():
        #        if file.name == save_file:
        #            raise ValueError("Such file already exists in this directory")

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

    params.set_params(P=20)
    print(params.P)

    params.save_preset("params presets/my presets/test.json")
    params.load_preset("params presets/my presets/test.json")
    print(params.P)

    params1 = Params()
    print(params1.P)

    print(params)
    print(params1)