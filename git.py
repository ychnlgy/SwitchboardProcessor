#!/usr/bin/python3

import os, sys
    
def pipeline(args):
    os.system("git add .")
    os.system("git commit -m \"%s\"" % " ".join(args))
    os.system("git pull origin master")
    os.system("git push origin master")

def main(username):
    args = sys.argv[1:]
    if not args:
        raise SystemExit("No action - provide a comment.")
    pipeline(args)

if __name__ == "__main__":
    main("ychnlgy")
