from os import fsync, path, mkdir

from util.TempFile import TempFile, TempFolder

def test_write():
    MSG = "Hello world!"
    fname = None
    with TempFile(".txt") as fname:
        with open(fname, "w") as f:
            f.write(MSG)
            fsync(f.fileno())
        with TempFile(".txt") as fname2:
            assert fname2 != fname
            with open(fname, "r") as f:
                assert f.read().rstrip() == MSG
    assert not path.isfile(fname)

def test_mkdir():
    with TempFolder() as name:
        assert path.isdir(name)
    assert not path.isdir(name)

def test_folderfile():
    with TempFolder() as folder:
        with TempFile() as fname:
            assert path.isdir(folder)
            assert path.isfile(fname)
        
        assert path.isdir(folder)
        assert not path.isfile(fname)
    
    assert not path.isdir(folder)
    assert not path.isfile(fname)

def test_multiple():
    with TempFile() as f1:
        with TempFile() as f2:
            
            assert path.isfile(f1)
            assert path.isfile(f2)
        
        assert path.isfile(f1)
        assert not path.isfile(f2)
    
    assert not path.isfile(f1)
    assert not path.isfile(f2)
