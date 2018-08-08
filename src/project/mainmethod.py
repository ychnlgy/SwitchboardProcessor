import sys, time

import lang
from util.Color import red, green, bold
from .Path import Path

ERROR = bold(red("ERROR: Non-zero return value %s\n"))
DONE = bold(green("DONE (%.3f s)"))
START = bold(green("Starting [%s]..."))

def mainmethod(f):
    DIR = Path.start(f)
    def mainmethod(fn):
        status(START % DIR)
        args = sys.argv[1:]
        result = -1
        t0 = time.time()
        try:
            result = fn(DIR, args)
        finally:
            if result is None or result == 0:
                dt = time.time() - t0
                status(DONE % dt)
            else:
                status(ERROR % result)
    return mainmethod

STATUS = bold("[ STATUS ] ")

def status(s):
    print(STATUS + s)
