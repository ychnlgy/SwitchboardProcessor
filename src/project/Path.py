from os import path, makedirs, remove
from shutil import rmtree

import lang

class Path(lang.Class):
    
    @staticmethod
    def start(fname):
        dname = path.normpath(path.dirname(fname))
        return Path(dname)
    
    def __init__(self, p):
        self.p = p
    
    def __str__(self):
        return self.p
    
    def __eq__(self, other):
        if type(other) == str:
            return self.p == other
        else:
            return other.p == self.p
    
    def __add__(self, p):
        p = path.join(self.p, path.normpath(p))
        return Path(p)
    
    def isfile(self):
        return path.isfile(self.p)
    
    def isdir(self):
        return path.isdir(self.p)
    
    def mkdir(self):
        makedirs(self.p)
    
    def rm(self):
        remove(self.p)
    
    def rmdir(self):
        rmtree(self.p)
