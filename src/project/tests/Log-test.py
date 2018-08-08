from project.Log import Log
from util.TempFile import TempFile

def test_log():
    with TempFile("temp_testfile") as f:
        with Log(f) as log:
            log.write("Jello")
            log.write("world")
        with open(f, "r") as fi:
            assert fi.read() == "Jello\nworld\n"
