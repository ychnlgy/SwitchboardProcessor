from interface.map.Searchable import Searchable

class Foo(Searchable):
    def get(self, key):
        return 1 if key=="password" else 0

def test_get():
    foo = Foo()
    assert foo["hack"] == 0
    assert foo["password"] == 1
