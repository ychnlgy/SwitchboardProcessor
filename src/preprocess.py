from tqdm import tqdm

from os import path, listdir, makedirs, system
from util.Struct import Struct
from util.Util import intround
from util.TempFile import TempFile
from filesys.WavFile import WavFile
from filesys.io import xmlparse

from scipy.io import wavfile

NCOLS = 80

PHONES = "nxt_switchboard_ann/xml/phones/sw{}.{}.phones.xml"

Entry = Struct("id", "rate", "waveA", "waveB", "phoneA", "phoneB")
PhonemeSlice = Struct("value", "start", "end")

def preprocess(sph2pipe, root, wavroot, target):
    entries = list(collectWavs(sph2pipe, root, wavroot, target))
    for entry in tqdm(entries, desc="Loading data", ncols=NCOLS):
        sliceIntoWaves(entry.id + "-A", entry.phoneA, entry.waveA, entry.rate, target)
        sliceIntoWaves(entry.id + "-B", entry.phoneB, entry.waveB, entry.rate, target)

def collectWavs(sph2pipe, root, wavroot, target):
    phones = path.join(root, PHONES)
    skipped = 0
    total = 0
    
    CONVERT_SPH = "%s -p -f wav %s %s"

    for f in listdir(wavroot):
        if f.startswith("swb1_"):
            p = path.join(wavroot, f, "data")
            for wav in tqdm(listdir(p), desc=f, ncols=80):
                total += 1
                sw0num, ext = wav.split(".")
                assert sw0num.startswith("sw0")
                assert ext == "sph"
                num = sw0num[3:]
                assert num.isdigit()
                    
                fname = path.join(p, wav)
                pfileA = phones.format(num, "A")
                pfileB = phones.format(num, "B")
                if not path.isfile(pfileA) or not path.isfile(pfileB):
                    skipped += 1
                    continue
                    
                with TempFile(num + ".wav") as wavf:
                    inpf = path.join(p, wav)
                    system(CONVERT_SPH % (sph2pipe, inpf, wavf))
                    assert path.isfile(wavf)
                    rate, data = wavfile.read(wavf)
                
                waveA = data[:,0]
                waveB = data[:,1]
                
                yield Entry(num, rate, waveA, waveB, pfileA, pfileB)
                
    print("Skipped %d/%d files." % (skipped, total))

def sliceIntoWaves(num, phonef, wave, rate, target):
    for phoneSlice in parsePhoneFile(phonef, rate):
        dname = path.join(target, phoneSlice.value)
        if not path.isdir(dname):
            makedirs(dname)
        
        fname = path.join(dname, "%s-%s-%s.wav" % (num, phoneSlice.start, phoneSlice.end))
        assert not path.isfile(fname)
        
        wavfile.write(fname, rate, wave[phoneSlice.start:phoneSlice.end])

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
        if len(args) != 4:
            raise SystemExit("Input input phoneme and wave folders, and output directory.")
        preprocess(*args)
