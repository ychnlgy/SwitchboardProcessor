import lang

class Boolean:
    def __bool__(self):
        return self.bool()
    
    @lang.abstract
    def bool(self):
        "Returns its boolean evaluation."
