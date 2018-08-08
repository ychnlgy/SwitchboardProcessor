import pytest
from util.Util import *

def test_fun():
    
    with pytest.raises(NotImplementedError):
        abstract()
        
    assert key((0, 2)) == 0
    assert value((0, 2)) == 2
