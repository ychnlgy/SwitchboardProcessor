from os import path, remove, makedirs
from shutil import rmtree

import lang
from interface.Context import Context
from filesys.io import write, touch, touchdir

TEMP = ".temp%s"

class TempFile(lang.Class, Context):
    def init(self, ext=""):
        self.ext = ext

    def __enter__(self):
        self.name = self.makeUniqueName(self.ext)
        self.makeExist()
        return self.name

    # === PRIVATE ===
    
    def makeExist(self):
        touch(self.name)
    
    def exists(self):
        return path.exists(self.name)
    
    def makeUniqueName(self, ext):
        temp = TEMP + ext
        name = temp % ""
        i = 1
        while path.exists(name):
            i += 1
            name = temp % i
        return name
    
    def delete(self):
        remove(self.name)
    
    def exit(self, *args):
        if self.exists():
            self.delete()

class TempFolder(TempFile):

    def makeExist(self):
        touchdir(self.name)
    
    def delete(self):
        rmtree(self.name)
