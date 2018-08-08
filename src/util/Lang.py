def copyname(fn1, fn2):
    setattr(fn1, "__name__", fn2.__name__)
