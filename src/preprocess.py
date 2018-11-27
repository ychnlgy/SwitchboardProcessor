import numpy

from tqdm import tqdm

from os import path, listdir, makedirs, system
from util.Struct import Struct
from util.Util import intround
from util.TempFile import TempFile
from filesys.WavFile import WavFile
from filesys.io import xmlparse

from scipy.io import wavfile

from collections import Counter

NCOLS = 80

PHONES = "nxt_switchboard_ann/xml/phones/sw{}.{}.phones.xml"

#Entry = Struct("id", "rate", "waveA", "waveB", "phoneA", "phoneB")
#PhonemeSlice = Struct("value", "start", "end")
#MIN_LEN = 0
#MAX_LEN = 4480

def preprocess(sph2pipe, root, wavroot, target):
    dataf = target + ".npy"
    
    print("Saving to %s" % target)
    with open(target, "wb") as f:
        for entry in collectWavs(sph2pipe, root, wavroot):
            numpy.save(f, entry)

#    classcounter = Counter()
#    for d, label in alldata:
#        classcounter[label] += 1
#    
#    classf = target + "-class.txt"
#    form = "{: <20}"*2 + "\n"
#    with open(classf, "w") as f:
#        f.write(form.format("Class", "Count"))
#        for v, k in sorted([(v, k) for k, v in classcounter.items()]):
#            f.write(form.format(k, v))

def collectWavs(sph2pipe, root, wavroot):
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
                
                pA = list(parsePhoneFile(pfileA, rate))
                pB = list(parsePhoneFile(pfileB, rate))
                
                waveA = data[:,0]
                waveB = data[:,1]
                
                yield numpy.array([num, rate, waveA, waveB, pA, pB], dtype=object)
                
    print("Skipped %d/%d files." % (skipped, total))

#def sliceIntoWaves(phonef, wave, rate):
#    for phoneSlice in parsePhoneFile(phonef, rate):
#        
#        d = phoneSlice.end - phoneSlice.start
#        if d <= MIN_LEN or d >= MAX_LEN:
#            continue
#        
#        yield [wave[phoneSlice.start:phoneSlice.end], phoneSlice.value]

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
        yield (child.text, s, e)

if __name__ == "__main__":
    
    from project.mainmethod import mainmethod
    
    @mainmethod(__file__)
    def main(DIR, args):
        if len(args) != 4:
            raise SystemExit("Input input phoneme and wave folders, and output directory.")
        preprocess(*args)
