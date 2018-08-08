from fnmatch import fnmatch
from os import listdir, path

def blob(root, include=["*"], exclude=[], depth=-1, iterdir=False):
    if path.isdir(root):
        for pname in listdir(root):
            p = path.join(root, pname)
            if not matches(p, exclude):
                if path.isdir(p):
                    if matches(p, include) and iterdir:
                        yield p
                    if depth:
                        for f in blob(p, include, exclude, depth-1, iterdir):
                            yield f
                elif matches(p, include):
                    yield p

# === PRIVATE ===

def matches(p, patterns):
    for pattern in patterns:
        if fnmatch(p, pattern):
            return True
    return False
