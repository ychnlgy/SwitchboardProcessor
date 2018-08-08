import lang

def Struct(*fields):

    default = [(f, None) for f in fields]

    class _Struct(lang.Class):
        def init(self, *args, **kwargs):
            d = dict(default)
            d.update(zip(fields, args))
            d.update(kwargs)
            self.__dict__.update(d)
        
    return _Struct
