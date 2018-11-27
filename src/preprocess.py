import numpy, os

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
SYLLABLES = "nxt_switchboard_ann/xml/syllables/sw{}.{}.syllables.xml"

#Entry = Struct("id", "rate", "waveA", "waveB", "phoneA", "phoneB")
#PhonemeSlice = Struct("value", "start", "end")
#MIN_LEN = 0
#MAX_LEN = 4480

def preprocess(sph2pipe, root, wavroot, target):
    dataf = target + ".npy"
    
    print("Saving to %s" % dataf)
    with open(dataf, "wb") as f:
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
    syllables = path.join(root, SYLLABLES)
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
                
                sfileA = syllables.format(num, "A")
                sfileB = syllables.format(num, "B")
                
                if not path.isfile(pfileA) or not path.isfile(pfileB) or not path.isfile(sfileA) or not path.isfile(sfileB):
                    skipped += 1
                    continue
                    
                with TempFile(num + ".wav") as wavf:
                    inpf = path.join(p, wav)
                    system(CONVERT_SPH % (sph2pipe, inpf, wavf))
                    assert path.isfile(wavf)
                    rate, data = wavfile.read(wavf)
                
                pA = list(parsePhoneFile(pfileA, rate))
                pB = list(parsePhoneFile(pfileB, rate))
                
                sA = list(parseSyllableFile(sfileA))
                sB = list(parseSyllableFile(sfileB))
                
                waveA = data[:,0]
                waveB = data[:,1]
                
                yield numpy.array([num, rate, waveA, waveB, pA, pB, sA, sB], dtype=object)
                
    print("Skipped %d/%d files." % (skipped, total))

#def sliceIntoWaves(phonef, wave, rate):
#    for phoneSlice in parsePhoneFile(phonef, rate):
#        
#        d = phoneSlice.end - phoneSlice.start
#        if d <= MIN_LEN or d >= MAX_LEN:
#            continue
#        
#        yield [wave[phoneSlice.start:phoneSlice.end], phoneSlice.value]

niteid = "{http://nite.sourceforge.net/}"

def parsePhoneFile(phonef, rate):
    root = xmlparse(phonef)
    assert root.tag == niteid + "phoneme_stream"
    start = niteid + "start"
    end = niteid + "end"
    nid = niteid + "id"
    for child in root:
        assert child.tag == "ph"
        s = intround(float(child.get(start))*rate)
        e = intround(float(child.get(end))*rate)
        yield (child.text, s, e, child.get(nid))

def parseSyllableFile(syllablef):
    root = xmlparse(syllablef)
    for child in root:
        href = child[0].attrib["href"]
        phonef, pid = href.split("#")
        assert path.basename(syllablef).replace(os.sep, ".") == phonef.replace(".phones.", ".syllables.")
        ids = pid.split("..")
        if len(ids) == 1:
            yield parseOnePhone(ids[0])
        else:
            yield parseMultiPhones(ids)

def parseOnePhone(pid, return_template=False):
    assert pid.startswith("id(") and pid.endswith(")")
    key = pid[3:-1]
    ms, ph = key.split("_")
    assert ph.startswith("ph")
    phn = int(ph[2:])
    if return_template:
        template = ms + "_ph%d"
        return phn, template
    else:
        return [key]

def parseMultiPhones(ids):
    assert len(ids) == 2
    key1, phn1, template1 = parseOnePhone(ids[0], return_template=True)
    key2, phn2, template2 = parseOnePhone(ids[1], return_template=True)
    assert template1 == template2
    keys = [(template1 % i) for i in range(phn1, phn2+1)]
    return keys

if __name__ == "__main__":
    
    from project.mainmethod import mainmethod
    
    @mainmethod(__file__)
    def main(DIR, args):
        if len(args) != 4:
            raise SystemExit("Input input phoneme and wave folders, and output directory.")
        preprocess(*args)
