from filesys.blob import blob
from project.Path import Path

DIR = Path.start(__file__)
DATA = DIR + "data/blob"

SAMPLE = DATA + "sample.xml"
TEST = DATA + "test.xml"
FOLDER = DATA + "folder"

INIT = "__init__.py"

INIT1 = FOLDER + INIT

SUB1 = FOLDER + "sub1"
SUB2 = FOLDER + "sub2"

SUBSUB1 = SUB1 + "subsub1"
SUBSUB2 = SUB1 + "subsub2"
SUBFILE1 = SUB1 + "File"
SUBFILE2 = SUB1 + "File 2"
SUBSUBFILE = SUBSUB1 + "File"
SUBSUBFILE2 = SUBSUB1 + "File 2"
SUBSUB2FILE = SUBSUB2 + "File"

SUB2INIT = SUB2 + INIT
SUB2INIT2 = SUB2 + "__init__ 2.py"

FILES = list(map(str, [
    TEST, 
    SAMPLE,
    SUBFILE1, 
    SUBFILE2, 
    SUBSUBFILE, 
    SUBSUBFILE2, 
    SUBSUB2FILE, 
    INIT1, 
    SUB2INIT, 
    SUB2INIT2
]))

def test_blob():
    root = str(DATA)
    a = set(blob(root))
    assert a == set(FILES)
    b = set(blob(root, include=["*.py"], exclude=[]))
    assert b == set(FILES[-3:])
    c = set(blob(root, exclude=["*.py"]))
    assert c == set(FILES[:-3])
    d = set(blob(root, exclude=["*.py"], depth=2))
    assert d == set(FILES[:4])
    e = set(blob(root, exclude=["*/sub2"]))
    assert e == set(FILES[:-2])
    f = set(blob(root, exclude=["*/sub2"], include=["*.py"]))
    assert f == {str(INIT1)}
    f = set(blob(root, exclude=["*/sub2"], include=["*.py", "*subsub1"], iterdir=True))
    assert f == {str(INIT1), str(SUBSUB1)}
