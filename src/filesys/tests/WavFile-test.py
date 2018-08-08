from filesys.WavFile import WavFile

from project.Path import Path
from util.TempFile import TempFile

DIR = Path.start(__file__)
SAMPLE = str(DIR + "data/sample.wav")

def test_wavfile():
    wav = WavFile.load(SAMPLE)
    assert wav.rate == 16000
    assert wav.data.shape == (1173,)
    assert len(wav) == 1173
    assert wav.at(100) == 400
    assert wav.at(101) == 892
    
    with TempFile() as t:
        wavs = wav[100:102]
        wavs.save(t)
        
        wav2 = WavFile.load(t)
        assert len(wav2) == 2
        assert wav2.at(0) == 400
        assert wav2.at(1) == 892
