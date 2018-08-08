import pytest

from util.Struct import Struct

def test_Struct():
    Fruit = Struct("vitc", "name")
    orange = Fruit(20, "orange")
    
    assert orange.vitc == 20
    assert orange.name == "orange"
    
    apple = Fruit()
    assert apple.vitc is None
    assert apple.name is None

    pear = Fruit(name="pear")
    assert pear.name == "pear"
    assert pear.vitc is None
