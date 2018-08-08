import lang

from interface.map.Searchable import Searchable
from interface.container.Sizable import Sizable

class DefaultMap(lang.Class, Searchable, Sizable):
    
    def init(self):
        self.data = {}
    
    @lang.abstract
    def default(self):
        "Returns the empty value for newly inserted keys."
    
    def get(self, key):
        try:
            return self.data[key]
        except KeyError:
            self.data[key] = self.default()
            return self[key]
    
    def items(self):
        return self.data.items()
    
    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def len(self):
        return len(self.data)
    
    def clear(self):
        self.data.clear()

class DefaultListMap(DefaultMap):
    def default(self):
        return []
