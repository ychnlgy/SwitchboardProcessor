import pytest

from lang import interface

@interface
class Foo:
    def foo(self):
        "Returns 1."

class Boo(Foo):
    def foo(self):
        return 1

def test_interface():
    foo = Foo()
    with pytest.raises(NotImplementedError):
        foo.foo()
        
    assert Boo().foo() == 1
