#!/usr/bin/python

import numpy, scipy, math
import scikits.talkbox

import scipy.io.wavfile

def main(fname):
    rate, data = scipy.io.wavfile.read(fname)
    print(get_formants(rate, data))

def get_formants(rate, data):

    data = data[4879:9200]

    # Get Hamming window.
    N = len(data)
    w = numpy.hamming(N)

    # Apply window and high pass filter.
    x1 = data * w
    x1 = scipy.signal.lfilter([1], [1., 0.63], x1)

    # Get LPC.
    A, e, k = scikits.talkbox.lpc(x1, 2 + rate/1000)

    # Get roots.
    rts = numpy.roots(A)
    rts = [r for r in rts if numpy.imag(r) >= 0]

    # Get angles.
    angz = numpy.arctan2(numpy.imag(rts), numpy.real(rts))

    # Get frequencies.
    frqs = sorted(angz * (rate / (2 * math.pi)))

    return frqs
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1])
