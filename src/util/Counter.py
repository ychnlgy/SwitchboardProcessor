import lang

from interface.Context import Context

class Counter(lang.Class, Context):

    START = 0
    class Stop(Exception): pass

    def init(self, stop):
        self.stop = stop
        self.tick = Counter.START
    
    def enter(self):
        self.reset()
    
    def exit(self, typ, val, tcb):
        if typ is None or typ == Counter.Stop:
            return True # ignore these exceptions.
        else:
            return False
    
    def check(self, b):
        if b:
            self.update()
        else:
            self.reset()
    
    def reset(self):
        self.tick = Counter.START
    
    def update(self):
        self.tick += 1
        if not self.tick < self.stop:
            raise Counter.Stop
