ENDC = '\033[0m'

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def green(s):
    return color(GREEN, s)

def red(s):
    return color(FAIL, s)

def bold(s):
    return color(BOLD, s)

def color(c, s):
    return c + s + ENDC
