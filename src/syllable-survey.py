from os import path, listdir
import xml.etree.ElementTree as ET

NITE = "{http://nite.sourceforge.net/}"
NITE_ID = NITE + "id"

NITE_START = NITE + "start"
NITE_END = NITE + "end"

SYLLABLE = "syllable"
PHONE = "ph"
HREF = "href"

PHONE_NAME = None
PHONE_FILE = None

def main():
    import sys
    args = dict([a.split("=") for a in sys.argv[1:]])
    p = args["path"]
    phonedir = path.join(p, "phones")
    syllable = path.join(p, "syllables")
    for f in listdir(syllable):
        fname = path.join(syllable, f)
        for phones in parseSyllableFile(fname, phonedir):
            print(phones)
            input("Next?")

def xmlparse(fname):
    return ET.parse(fname).getroot()

def parseSyllableFile(fname, phonedir):
    root = xmlparse(fname)
    assert len(root.attrib) == 1
    nite = list(root.attrib.keys())[0]
    assert nite == NITE_ID
    
    bname = path.basename(fname)
    name, speaker, dtype, ext = bname.split(".")
    for child in root:
        assert child.tag == SYLLABLE
        phones = seekPhoneFile(child, phonedir)
        yield phones # list of string phones

def seekPhoneFile(child, phonedir):
    nodes = list(child)
    assert len(nodes) == 1
    phoneRef = nodes[0].attrib[HREF]
    phonef, ids = phoneRef.split("#")
    phonefname = path.join(phonedir, phonef)
    if phonefname != PHONE_NAME:
        PHONE_NAME = phonefname
        PHONE_FILE = parsePhoneFile(phonefname)
    phones = collectPhones(ids)
    return [PHONE_FILE[ph] for ph in phones]

def collectPhones(ids):
    pieces = ids.split("..")
    if len(pieces) == 1:
        return [parseSinglePhone(pieces[0])[0]]
    else:
        assert len(pieces) == 2
        return parseTwoPhones(*pieces)

def parseSinglePhone(piece):
    assert piece.startswith("id(")
    assert piece.endswith(")")
    impt = piece[3:-1]
    ms, ph = impt.split("_")
    assert ms.startswith("ms")
    assert ph.startswith("ph")
    num = int(ph[2:])
    return impt, ms, num

def parseTwoPhones(p1, p2):
    id1, ms1, n1 = parseSinglePhone(p1)
    id2, ms2, n2 = parseSinglePhone(p2)
    assert ms1 == ms2
    nums = range(n1, n2+1)
    form = "%s_ph%%d" % ms1
    return [form % i for i in nums]

def parsePhoneFile(phonef):
    root = xmlparse(phonef)
    out = {}
    for child in root:
        assert child.tag == PHONE
        key = child.attrib[NITE_ID]
        assert key not in out
        assert child.text is not None
        out[key] = child.text
    return out

if __name__ == "__main__":
    main()
