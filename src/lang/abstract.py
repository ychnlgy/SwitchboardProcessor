from util.Lang import copyname

def abstract(fn):
    def wrapped(*args, **kwargs):
        raise NotImplementedError("Function \"%s\" is abstract yet not defined." % fn.__name__)
    copyname(wrapped, fn)
    return wrapped
