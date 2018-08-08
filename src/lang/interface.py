import lang

from .abstract import abstract

@lang.returnarg
def interface(obj):
    for k, v in obj.__dict__.items():
        if not k.startswith("_") and callable(v):
            setattr(obj, k, abstract(v))
