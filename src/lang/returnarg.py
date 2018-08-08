from util.Lang import copyname

def returnarg(fn):
    def wrapped(arg):
        fn(arg)
        return arg
    copyname(wrapped, fn)
    return wrapped
