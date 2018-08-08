from util.DefaultMap import DefaultMap, DefaultListMap

def test_defaultlist():
    d = DefaultListMap()
    assert d[8] == []
    d[8].append(6)
    d[7].append(5)
    d[7].append(4)
    assert sorted(d.keys()) == [7, 8]
    assert d[7] == [5, 4]
    assert d[8] == [6]
    assert sorted(d.items()) == [(7, [5, 4]), (8, [6])]
    assert len(d) == 2
    assert len(d.values()) == 2
    
    d.clear()
    assert list(d.items()) == []
