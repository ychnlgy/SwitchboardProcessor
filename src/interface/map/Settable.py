import lang

class Settable:
    
    def __setitem__(self, key, value):
        self.set(key, value)
    
    @lang.abstract
    def set(self, key, value):
        "Sets self to map the input key to its new value."
