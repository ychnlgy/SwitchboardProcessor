import lang
from interface.Context import Context
from util.Util import none, stdout

class Log(lang.Class, Context):
    def __init__(self, fname, verbose=True):
        self.fname = fname
        self.printf = stdout if verbose else none
    
    def enter(self):
        self.file = open(self.fname, "w")
        return self
    
    def exit(self, *args):
        self.file.flush()
        self.file.close()
    
    def write(self, s):
        s += "\n"
        self.printf(s)
        self.file.write(s)
