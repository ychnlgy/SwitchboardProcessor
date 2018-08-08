from util.OneTime import OneTime

def test_once():
    b = OneTime()
    if not b:
        assert False
    if b:
        assert False
