import lang

class Sizable:
    def __len__(self):
        return self.len()

    @lang.abstract
    def len(self):
        "Returns the size of this container."
