import lang
from interface.serial.Jsonable import Jsonable
from util.TempFile import TempFile

class Foo(lang.Class, Jsonable):
    def init(self, a, b):
        self.a = a
        self.b = b

    def fromObj(self, obj):
        (
            self.a,
            self.b
        ) = obj
    
    def json(self):
        return [self.a, self.b]
    
def test_json():
    with TempFile(".temp") as fname:
        foo = Foo(2, 3)
        foo.dump(fname)
    
        foo2 = Foo(5, 6)
        assert foo2.a == 5
        assert foo2.b == 6
        
        foo2.load(fname)
        assert foo2.a == 2
        assert foo2.b == 3
