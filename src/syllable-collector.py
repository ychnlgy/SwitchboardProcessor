#!/usr/bin/python3

import numpy, tqdm, itertools, collections, os, random

import scipy.signal

import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot

from sampler import create_keepset

SAMPLES = 5
ADDITIONAL_SAMPLES = 20

NPERSEG = 256
NOVERLAP = 255
NFFT = 512

def load(npy):
    i = 0
    with tqdm.tqdm(itertools.count(), desc="Loading data", ncols=80) as bar:
        with open(npy, "rb") as f:
            for i in bar:
                try:
                    yield numpy.load(f)
                    
                    # TODO: remove
                    #i += 1
                    #if i > 10:
                    #    break
                except OSError:
                    break

# syllables are lists of phonemes
# we want to check if the syllable is what we seek
# we want to know the range of the syllable
# we want to collect the spectrograms of the audio in these ranges

def map_phones(phn):
    "phn_id -> value, start, end"
    out = {}
    for value, start, end, phn_id in phn:
        assert phn_id not in out
        out[phn_id] = (value, start, end)
    return out

def syllable2phone(mapped_phones, syllables, kept):
    for phn_ids in syllables:
        phns = [mapped_phones[phn_id] for phn_id in phn_ids]
        key = tuple([v for v, s, e in phns])
        if key in kept:
            s = phns[0][1]
            e = phns[-1][2]
            if e - s > NPERSEG:
                yield key, s, e, [e[-1] for e in phns]

def slice_audio(syllables, wave):
    for key, s, e, ends in syllables:
        slc = wave[s:e+1]
        yield ", ".join(key), slc, ends

def to_spectrogram(audio_slices, rate, n=SAMPLES):
    #assert len(audio_slices) > n
    random.shuffle(audio_slices)
    slcs = audio_slices[:n+ADDITIONAL_SAMPLES]
    for slc, ends in slcs:
        f, t, spec = scipy.signal.spectrogram(slc, fs=rate, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NFFT)
        dt = len(t)/len(slc)
        conv = numpy.array([min(int(round(e*dt)), len(t)-1) for e in ends])
        marked = numpy.copy(spec)
        marked[:,conv] = numpy.min(marked)
        yield f, t, spec, marked

def average_spectrograms(specs):
    others = []
    longest = None
    for spec in specs:
        if longest is None or spec.shape[1] > longest.shape[1]:
            others.append(longest)
            longest = spec
        else:
            others.append(spec)
    longest = numpy.copy(longest)
    assert longest is not None
    for arr in others:
        if arr is not None:
            longest[-arr.shape[0]:,:arr.shape[1]] += arr[:,:]
    return longest/(len(others)+1)

def fill_spec(shape, spec):
    out = numpy.zeros(shape)
    out += numpy.min(spec)
    out[-spec.shape[0]:, :spec.shape[1]] = spec[:,:]
    return out

EPS = 1e-12

def plot(axis, spec, t, f, lowest, highest):
    if lowest <= 0:
        lowest = EPS
    lowest, highest = 10*numpy.log10(lowest), 10*numpy.log10(highest)
    spec[spec <= 0] = EPS
    axis.pcolormesh(t, f, 10*numpy.log10(spec), cmap="hot", vmax=highest, vmin=lowest)

def main(npy):
    keepset = create_keepset()
    
    data = list(load(npy))
    
    out = collections.defaultdict(list)
    
    for num, rate, waveA, waveB, pA, pB, sA, sB in tqdm.tqdm(data, desc="Processing", ncols=80):
        mapA = map_phones(pA)
        mapB = map_phones(pB)
        sylA = syllable2phone(mapA, sA, keepset)
        sylB = syllable2phone(mapB, sB, keepset)
        
        for key, slc, ends in slice_audio(sylA, waveA):
            out[key].append((slc, ends))
        
        for key, slc, ends in slice_audio(sylB, waveB):
            out[key].append((slc, ends))
    
    NCOLS = SAMPLES
    NROWS = 4
    
    OUTD = "syllable_spectrograms"
    if not os.path.isdir(OUTD):
        os.makedirs(OUTD)
        
    FPATH = os.path.join(OUTD, "%d.png")
    
    sap = sorted(out.items())
    idx = range(len(sap)//NROWS+1)
    
    for i in tqdm.tqdm(idx, desc="Creating spectrograms", ncols=80):
        grp = sap[i*NROWS:(i+1)*NROWS]
        fname = FPATH % i
        if len(grp) == 0:
            break
        
        fig, axes = pyplot.subplots(nrows=NROWS, ncols=NCOLS+1)
        fig.set_size_inches(22, 12)
        
        for j, (key, slcs) in enumerate(grp):
            axes[j, 0].set_ylabel(key)
            specs = []
            draw = []
            t_map = {}
            f_map = {}
            highest = -float("inf")
            lowest = float("inf")
            for k, (f, t, spec, marked) in enumerate(to_spectrogram(slcs, rate), 1):
                specs.append(spec)
                
                low = numpy.min(spec)
                high = numpy.max(spec)
                
                if high > highest:
                    highest = high
                if low < lowest:
                    lowest = low
                
                t_map[spec.shape[1]] = t
                f_map[spec.shape[0]] = f
                if k <= SAMPLES:
                    draw.append(marked)
            
            avg = average_spectrograms(specs)
            t = t_map[avg.shape[1]]
            f = f_map[avg.shape[0]]
            plot(axes[j,0], avg, t, f, lowest, highest)
            for k in range(SAMPLES):
                spec = fill_spec(avg.shape, draw[k])
                plot(axes[j, k+1], spec, t, f, lowest, highest)
            
        axes[0, 0].set_title("Average")
        for i, axis in enumerate(axes[0,1:]):
            axis.set_title("Sample %d" % i)
        pyplot.savefig(fname, bbox_inches="tight")
        pyplot.close()
        #input("Saved one")

if __name__ == "__main__":
    main("../../switchboard-data.npy")

