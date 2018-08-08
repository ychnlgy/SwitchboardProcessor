import pytest
from util.Counter import Counter

def count(do, expect):
    i = 0
    with Counter(10) as counter:
        for i in range(do):
            counter.update()
    assert i == expect

def test_counter():
    count(5, 4)
    count(10, 9)
    count(11, 9)
    count(100, 9)

def iterate():
    for i in range(7):
        yield i
    for i in range(8, 3, -1):
        yield i
    for i in range(2, 12):
        yield i

def test_check():
    i = 0
    j = 0
    with Counter(5) as counter:
        for j in iterate():
            counter.check(j > 5)
            i += 1
    assert j == 10
    assert i == 20

def test_exiterror():
    with pytest.raises(NotImplementedError):
        with Counter(4) as counter:
            raise NotImplementedError
