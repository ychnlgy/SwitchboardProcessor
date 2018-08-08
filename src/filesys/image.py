from scipy.misc import imread
from PIL import Image

def parse(fname):
    return Image.open(fname)

def numparse(fname):
    return imread(fname)
