from interface.sequence.Iterable import Iterable

class Foo(Iterable):
    def iter(self):
        for i in range(10):
            yield i

def test_iter():
    assert list(iter(Foo())) == list(range(10))
