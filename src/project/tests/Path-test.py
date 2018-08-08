import pytest
from os import path

from project.Path import Path
from filesys.io import writeSync

DIR = Path.start(__file__)
DATA = DIR + "data"
FILE = DATA + "File"
FOLD = DATA + "folder"
TEMP = DATA + "temp"
TMPF = TEMP + "file.py"

N1 = [".", "hello", ".", "joke", "..", "fool.txt"]
P1 = path.join(*N1)
N2 = ["hello", "oops.foo"]
P2 = path.join(*N2)
N3 = ["hello", "you", "silly"]
P3 = path.join(*N3)

def test_start():
    d = Path.start(P1)
    assert d == N1[1]
    d2 = Path.start(P2)
    assert d == d2
    d3 = Path.start(P3)
    assert d3 != d
    assert d3 != d2

def test_add():
    p = Path(N2[0])
    p2 = p + P1
    assert p2 == "hello/hello/fool.txt"

def test_os():
    print(str(FILE))
    assert path.isfile(str(FILE))
    assert FILE.isfile()
    assert not FOLD.isfile()
    assert FOLD.isdir()
    assert not TEMP.isdir()
    assert not TEMP.isfile()
    assert not TMPF.isdir()
    assert not TMPF.isfile()
    TEMP.mkdir()
    assert TEMP.isdir()
    writeSync(str(TMPF), "hello")
    assert TMPF.isfile()
    TMPF.rm()
    assert not TMPF.isfile()
    TEMP.rmdir()
    assert not TEMP.isdir()
