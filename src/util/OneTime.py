import lang

from interface.Boolean import Boolean

class OneTime(lang.Class, Boolean):
    def init(self):
        self.b = 1
    
    def bool(self):
        out = bool(self.b)
        if out:
            self.toggle()
        return out
    
    def toggle(self):
        self.b = 1 - self.b
