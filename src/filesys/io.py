from os import fsync, makedirs
from util.Util import none
import xml.etree.ElementTree as ET

def parse(fname):
    with open(fname, "r") as f:
        for line in f:
            yield line.rstrip()

def read(fname):
    with open(fname, "r") as f:
        return f.read()

def touch(fname):
    write(fname, "")

def touchdir(dname):
    makedirs(dname)

def xmlparse(fname):
    tree = ET.parse(fname)
    return tree.getroot()

def write(fname, text, fn=none):
    with open(fname, "w") as f:
        f.write(text)
        none(f)

def writeSync(fname, text):
    write(fname, text, sync)

def sync(f):
    fsync(f.fileno())
