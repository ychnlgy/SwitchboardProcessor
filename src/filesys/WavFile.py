from scipy.io import wavfile

import lang
from interface.container.Sizable import Sizable
from interface.map.Searchable import Searchable

class WavFile(lang.Class, Sizable, Searchable):

    @staticmethod
    def load(fname):
        return WavFile(*wavfile.read(fname))
    
    def len(self):
        return len(self.data)

    def get(self, slc):
        return WavFile(self.rate, self.data[slc])
    
    def at(self, i):
        return self.data[i]
        
    def save(self, fname):
        wavfile.write(fname, self.rate, self.data)
    
    # === PRIVATE ===
    
    def init(self, rate, data):
        self.rate = rate
        self.data = data

