import lang

class Iterable:
    
    def __iter__(self):
        return self.iter()
    
    @lang.abstract
    def iter(self):
        "Iterates through its data."
