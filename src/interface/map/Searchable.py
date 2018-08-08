import lang

class Searchable:

    def __getitem__(self, key):
        return self.get(key)
    
    @lang.abstract
    def get(self, key):
        "Returns the value associated with this key."
