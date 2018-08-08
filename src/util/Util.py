import sys

stdout = sys.stdout.write

def key(kv):
    return kv[0]

def value(kv):
    return kv[1]

def none(*args, **kwargs):
    return

def abstract(*args, **kwargs):
    raise NotImplementedError

def intround(v):
    return int(round(v))
