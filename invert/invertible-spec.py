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

def spectrogram(rate, data, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NPERSEG):
    return scipy.signal.stft(data, fs=rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)

def inverse_spec(rate, spec, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NPERSEG):
    return scipy.signal.istft(spec, fs=rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)

def from_spectrogram(rate, spec, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NPERSEG, iters=100):
    length = scipy.signal.istft(spec, rate, nperseg=nperseg)[1].shape[0]
    x = numpy.random.normal(size=length)
    for i in range(iters):
        X = scipy.signal.stft(x, rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)[2]
        Z = spec * numpy.exp(numpy.angle(X) * 1j)
        x = scipy.signal.istft(Z, rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)[1]
    return numpy.real(x)

def main():
    rate, data = load("happy.wav")
    spec = pretty_spectrogram(data, step_size=1)
    pyplot.imshow(spec, cmap="hot", interpolation="nearest", aspect="auto")
    pyplot.savefig("spec.png")
    
    datap = invert_pretty_spectrogram(spec, step_size=1, n_iter=100)
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

    from matplotlib import pyplot

    def plot(f, t, spec, name):
        pyplot.pcolormesh(t, f, 10*numpy.log10(numpy.abs(spec)), cmap="hot")
        pyplot.savefig(name + ".png", bbox_inches="tight")
        pyplot.clf()
    
    def stat(spec):
        spec = numpy.abs(spec)
        print(spec.shape, numpy.min(spec), numpy.max(spec), numpy.mean(spec))

    main()
