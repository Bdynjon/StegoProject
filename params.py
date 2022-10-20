import json


class Params:
    def __init__(self):
        self.P = 5
        self.HF = (9, 15)
        self.LF = (1, 6)
        self.Pl = 2600
        self.Ph = 40
        self.rows = (7, 8)

    def set_params(self, P=None, HF=None, LF=None, Pl=None, Ph=None, rows=None):
        self.P = P if P else self.P
        self.HF = HF if HF else self.HF
        self.LF = LF if LF else self.LF
        self.Pl = Pl if Pl else self.Pl
        self.Ph = Ph if Ph else self.Ph
        self.rows = rows if rows else self.rows

    def save_preset(self, path: str = "params presets/test.json"):
        param_dict = {
            "P": self.P,
            "HF": self.HF,
            "LF": self.LF,
            "Pl": self.Pl,
            "Ph": self.Ph,
            "rows": self.rows
        }

        with open(path, "w") as param_file:
            json.dump(param_dict, param_file, indent=2)

    def load_preset(self, path: str = "params presets/test.json"):
        with open(path, "r") as param_file:
            param_dict = json.load(param_file)

        self.set_params(param_dict["P"], param_dict["HF"], param_dict["LF"], param_dict["Pl"], param_dict["Ph"],
                        param_dict["rows"])


if __name__ == "__main__":
    params = Params()
    params.save_preset()
    params.load_preset()

    print(params.P)
