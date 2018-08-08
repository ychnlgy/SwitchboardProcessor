import pytest, lang

class Foo:

    @lang.abstract
    def foo(self):
        "Doc."

class Boo(Foo):

    def foo(self):
        return 1

def test_abstractuse():
    
    foo = Foo()
    
    with pytest.raises(NotImplementedError):
        foo.foo()
    
    boo = Boo()
    assert boo.foo() == 1
