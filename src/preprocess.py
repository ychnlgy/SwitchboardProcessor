from tqdm import tqdm

from os import path, listdir, makedirs
from project.Path import Path
from util.Struct import Struct
from util.Util import intround
from filesys.WavFile import WavFile
from filesys.io import xmlparse

NCOLS = 80

PHONES = "nxt_switchboard_ann/xml/phones/sw{num}.{speaker}.phones.xml"

Entry = Struct("id", "wave", "phoneA", "phoneB")
PhonemeSlice = Struct("value", "start", "end")

def preprocess(root, target):
    entries = list(tqdm(collectWavs(root), desc="Previewing data", ncols=NCOLS))
    for entry in tqdm(entries, desc="Loading data", ncols=NCOLS):
        sliceIntoWaves(entry.id + "-A", entry.phoneA, entry.wave, target)
        sliceIntoWaves(entry.id + "-B", entry.phoneB, entry.wave, target)

def collectWavs(root):
    phones = str(Path(root) + PHONES)
    for f in listdir(root):
        if f.startswith("Disc"):
            p = path.join(root, f)
            for wav in listdir(p):
                num, ext = wav.split(".")
                assert num.isdigit()
                assert ext == ".wav"
                fname = path.join(p, wav)
                pfileA = PHONES.format(num, "A")
                pfileB = PHONES.format(num, "B")
                yield Entry(num, fname, pfileA, pfileB)

def sliceIntoWaves(num, phonef, wavf, target):
    wave = WavFile.load(wavf)
    for phoneSlice in parsePhoneFile(phonef, wav.rate):
        dname = path.join(target, phoneSlice.value)
        if not path.isdir(dname):
            makedirs(dname)
        
        fname = path.join(dname, "%s-%s-%s.wav" % (num, phoneSlice.start, phoneSlice.end))
        assert not path.isfile(fname)
        
        wave[phoneSlice.start:phoneSlice.end].save(fname)

def parsePhoneFile(phonef, rate):
    root = xmlparse(phonef)
    niteid = "{http://nite.sourceforge.net/}"
    assert root.tag == niteid + "phoneme_stream"
    start = niteid + "start"
    end = niteid + "end"
    for child in root:
        assert child.tag == "ph"
        s = intround(float(child.get(start))*rate)
        e = intround(float(child.get(end)))
        yield PhonemeSlice(child.text, s, e)

if __name__ == "__main__":
    
    from project.Path import mainmethod
    
    @mainmethod
    def main(DIR, args):
        if len(args) != 2:
            raise SystemExit("Input input and output directories.")
        preprocess(*args)
