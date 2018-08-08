import lang, json

class Jsonable:

    def dump(self, fname):
        with open(fname, "w") as f:
            json.dump(self.json(), f)
    
    def load(self, fname):
        with open(fname, "r") as f:
            obj = json.load(f)
            self.fromObj(obj)

    @lang.abstract
    def fromObj(self, obj):
        "Loads features of obj into itself."

    @lang.abstract
    def json(self):
        "Returns the JSON form of itself."
