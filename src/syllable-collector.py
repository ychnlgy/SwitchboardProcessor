#!/usr/bin/python3

import numpy, tqdm, itertools, collections, os, random

import scipy.signal

import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot

from sampler import create_keepset

SAMPLES = 5

def load(npy):
    i = 0
    with open(npy, "rb") as f:
        for i in tqdm.tqdm(itertools.count(), desc="Loading data", ncols=80):
            try:
                yield numpy.load(f)
                
                # TODO: remove
                i += 1
                if i > 10:
                    break
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
            if s < e:
                yield key, s, e

def slice_audio(syllables, wave):
    for key, s, e in syllables:
        assert s >= 0 and len(wave) >= e
        slc = wave[s:e+1]
        yield ", ".join(key), slc

def to_spectrogram(audio_slices, rate, n=SAMPLES):
    assert len(audio_slices) > n
    random.shuffle(audio_slices)
    slcs = audio_slices[:n]
    for slc in slcs:
        yield scipy.signal.spectrogram(slc, fs=rate)

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
            longest[:arr.shape[0],:arr.shape[1]] += arr[:,:]
    return longest/(len(others)+1)

def main(npy):
    keepset = create_keepset()
    
    data = list(load(npy))
    
    out = collections.defaultdict(list)
    
    for num, rate, waveA, waveB, pA, pB, sA, sB in tqdm.tqdm(data, desc="Processing", ncols=80):
        mapA = map_phones(pA)
        mapB = map_phones(pB)
        sylA = syllable2phone(mapA, sA, keepset)
        sylB = syllable2phone(mapB, sB, keepset)
        
        for key, slc in slice_audio(sylA, waveA):
            out[key].append(slc)
        
        for key, slc in slice_audio(sylB, waveB):
            out[key].append(slc)
    
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
        nrows = len(grp)
        fig, axes = pyplot.subplots(nrows=nrows, ncols=NCOLS+1)
        fig.set_size_inches(22, 12)
        fname = FPATH % i
        for j, (key, slcs) in enumerate(grp):
            axes[j, 0].set_ylabel(key)
            specs = []
            longest_t = None
            for k, (f, t, spec) in enumerate(to_spectrogram(slcs, rate), 1):
                axes[j, k].pcolormesh(t, f, 10*numpy.log10(spec), cmap="hot")
                specs.append(spec)
                if longest_t is None or len(t) > len(longest_t):
                    longest_t = t
            avg = average_spectrograms(specs)
            axes[j, 0].pcolormesh(longest_t, f, 10*numpy.log10(avg), cmap="hot")
        axes[0, 0].set_title("Average")
        for i, axis in enumerate(axes[0,1:]):
            axis.set_title("Sample %d" % i)
        pyplot.savefig(fname, bbox_inches="tight")
        pyplot.clf()
        #input("Saved one")

if __name__ == "__main__":
    main("../../switchboard-data.npy")

