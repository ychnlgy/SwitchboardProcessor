from os import path, remove

from filesys.io import sync, parse, xmlparse, read
from project.Path import Path

F = "test-deleteme"
DIR = Path.start(__file__)
FILE = DIR + "data/blob/sample.xml"

def test_sync():
    hello = "hello"
    with open(F, "w") as f:
        f.write(hello)
        sync(f)
    assert path.isfile(F)
    for line in parse(F):
        assert line == hello
    assert hello == read(F)
    remove(F)

def test_xmlparse():
    root = xmlparse(str(FILE))
    children = list(root)
    assert len(children) == 3
    assert children[0].get("name") == "Liechtenstein"
