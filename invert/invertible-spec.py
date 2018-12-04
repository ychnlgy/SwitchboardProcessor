import numpy
import scipy.io.wavfile
import scipy.signal

from spec_invert import invert_pretty_spectrogram, pretty_spectrogram

NPERSEG = 256
NOVERLAP = 128

def load(fname):
    return scipy.io.wavfile.read(fname)

def save(fname, rate, data):
    scipy.io.wavfile.write(fname, rate, data)

def spectrogram(totaltime, rate, spec, nperseg=NPERSEG):
    freq = numpy.arange(spec.shape[1])/nperseg*rate/2
    time = numpy.arange(spec.shape[0])*(totaltime/spec.shape[0])
    return freq, time

def inverse_spec(rate, spec, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NPERSEG):
    return scipy.signal.istft(spec, fs=rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)

def from_spectrogram(rate, spec, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NPERSEG, iters=10):
    length = scipy.signal.istft(spec, rate, nperseg=nperseg)[1].shape[0]
    x = numpy.random.normal(size=length)
    for i in range(iters):
        X = scipy.signal.stft(x, rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)[2]
        Z = spec * numpy.exp(numpy.angle(X) * 1j)
        x = scipy.signal.istft(Z, rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)[1]
    return numpy.real(x)

def shift_block(slc, ti, tj, fi, fj, dmax):
    mid = (tj + ti)//2
    std = tj-mid
    pyplot.plot(slc[mid])
    pyplot.savefig("original-mid.png")
    pyplot.clf()
    
    low = numpy.min(slc)
    for t in range(ti, tj):
        v = 1 - ((t - mid)/std)**2
        d = int(round(v * dmax))
        if d:
            shift(slc[t], fi, fj, d, low)
    
    pyplot.plot(slc[mid])
    pyplot.savefig("altered-mid.png")
    pyplot.clf()

def shift(slc, fi, fj, d, lowest):
    add = splice(slc, fi, fj, d, lowest)
    insert_spliced(add, slc, fi+d, fj+d)

def splice(slc, fi, fj, d, lowest):
    yj = slc[fj]
    yi = slc[fi]
    m = (yj - yi)/(fj - fi)
    intp = numpy.arange(fj-fi) * m + yi
    vals = slc[fi:fj] - intp
    slc[fj-abs(d):fj] = intp[-abs(d):]
    return vals

def insert_spliced(add, slc, fi, fj):
    slc[fi:fj] = (slc[fi:fj] + add)

def get_index_of_freq(freq, rate, nperseg=NPERSEG):
    return int(round(freq*2*nperseg/rate))

def main():
    rate, data = load("happy.wav")
    #f, t, spec = scipy.signal.spectrogram(data, fs=rate, nperseg=NPERSEG, noverlap=NOVERLAP)
    spec = pretty_spectrogram(data, step_size=1)
    f, t = spectrogram(len(data)/rate, rate, spec)
    
    i = get_index_of_freq(1700, rate)
    j = get_index_of_freq(2500, rate)
    
    shift_block(spec, 4879, 9200, i, j, -50)
    
    #spec[:,-100:] = numpy.min(spec)
    pyplot.pcolormesh(t, f, spec.T, cmap="hot", vmax=1)
    pyplot.colorbar()
    pyplot.savefig("spec.png")
    pyplot.show()
    datap = invert_pretty_spectrogram(spec, step_size=1, n_iter=4)
    save("reconstruct.wav", rate, datap)
    
    #stat(spec)
    #plot(f, t, spec, "stft")
    
    #datap = from_spectrogram(rate, spec)
    #datap = invert_pretty_spectrogram(spec, log=False, fft_size=NPERSEG, step_size=NOVERLAP)
    #save("happy-reconstructed.wav", rate, datap)
    
#    f, t, spec = scipy.signal.spectrogram(data, fs=rate, nperseg=NPERSEG, noverlap=NOVERLAP)
#    stat(spec)
#    
#    plot(f, t, spec, "spectrogram")

if __name__ == "__main__":

    import matplotlib
    #matplotlib.use("agg")
    from matplotlib import pyplot

    def plot(f, t, spec, name):
        pyplot.pcolormesh(t, f, 10*numpy.log10(numpy.abs(spec)), cmap="hot")
        pyplot.savefig(name + ".png", bbox_inches="tight")
        pyplot.clf()
    
    def stat(spec):
        spec = numpy.abs(spec)
        print(spec.shape, numpy.min(spec), numpy.max(spec), numpy.mean(spec))

    main()
