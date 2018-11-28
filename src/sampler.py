#!/usr/bin/python3

FILE = "syllable-survey.txt"

def create_keepset(f=FILE)
    kept = keep_largecontrib(list(parse(f)))
    return {sids for stype, count, sids in kept}

# === PRIVATE ===

def parse(fname):
    with open(fname, "r") as f:
        for line in f:
            line = line.rstrip()
            pieces = list(filter(None, line.split(" ")))
            stype = pieces[0]
            assert set(stype).issubset({"V", "C"})
            count = int(pieces[1])
            sids = [s.rstrip(",") for s in pieces[2:]]
            yield stype, count, tuple(sids)

def count(data):
    total = 0
    for stype, count, sids in data:
        total += count
    return total

def keep_largecontrib(data, p=0.001):
    # keep those that contribute p or more
    total = count(data)
    out = []
    thres = int(total * p)
    for e in data:
        if e[1] > thres:
            out.append(e)
    return out

if __name__ == "__main__":
    f = parse(FILE)
    
    data = list(f)
    data = keep_largecontrib(data)
    
    print(data[0])
    print(data[1])
    print(len(data))
