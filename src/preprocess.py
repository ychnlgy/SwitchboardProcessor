from tqdm import tqdm

from os import path, listdir, makedirs
from util.Struct import Struct
from util.Util import intround
from filesys.WavFile import WavFile
from filesys.io import xmlparse

NCOLS = 80

PHONES = "nxt_switchboard_ann/xml/phones/sw{}.{}.phones.xml"

Entry = Struct("id", "wave", "phoneA", "phoneB")
PhonemeSlice = Struct("value", "start", "end")

def preprocess(root, wavroot, target):
    entries = list(collectWavs(root, wavroot))
    for entry in tqdm(entries, desc="Loading data", ncols=NCOLS):
        sliceIntoWaves(entry.id + "-A", entry.phoneA, entry.wave, target)
        sliceIntoWaves(entry.id + "-B", entry.phoneB, entry.wave, target)

def collectWavs(root, wavroot):
    phones = path.join(root, PHONES)
    skipped = 0
    total = 0
    for f in listdir(wavroot):
        if f.startswith("swb1_"):
            p = path.join(wavroot, f, "data")
            for wav in listdir(p):
                total += 1
                sw0num, ext = wav.split(".")
                assert sw0num.startswith("sw0")
                assert ext == "wav"
                num = sw0num[3:]
                assert num.isdigit()
                
                fname = path.join(p, wav)
                pfileA = phones.format(num, "A")
                pfileB = phones.format(num, "B")
                if not path.isfile(pfileA) or not path.isfile(pfileB):
                    skipped += 1
                    print(pfileA)
                    continue
                yield Entry(num, fname, pfileA, pfileB)
    input("Skipped %d/%d files (press enter to continue)." % (skipped, total))

def sliceIntoWaves(num, phonef, wavf, target):
    wave = WavFile.load(wavf)
    for phoneSlice in parsePhoneFile(phonef, wave.rate):
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
        e = intround(float(child.get(end))*rate)
        yield PhonemeSlice(child.text, s, e)

if __name__ == "__main__":
    
    from project.mainmethod import mainmethod
    
    @mainmethod(__file__)
    def main(DIR, args):
        if len(args) != 3:
            raise SystemExit("Input input phoneme and wave folders, and output directory.")
        preprocess(*args)
