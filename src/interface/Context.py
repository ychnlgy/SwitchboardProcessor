import lang

class Context:
    def __enter__(self):
        self.enter()
        return self
    
    def __exit__(self, *args):
        return self.exit(*args)
    
    @lang.abstract
    def enter(self):
        "Sets up self before entering a context."
    
    @lang.abstract
    def exit(self, *args):
        "Teardown self after exiting a context."
