import random
import getopt
import sys
import errno
import base64

optlist, args = getopt.getopt(sys.argv[1:], '?c:w:dhob6ks:X:N:', ["help"])
if len(args) > 0:
    sys.stderr.write("%s: Error: Unexpected command line argument '%s'.\n" % (sys.argv[0], args[0]))
    sys.exit(errno.EINVAL);
    

FMT_DEC = 0
FMT_HEX = 1
FMT_OCT = 2
FMT_BIN = 3
FMT_B64 = 4

def fmtbin(n, w):
    s = bin(n)[2:]
    while len(s) < w:
        s = "0" + s
    return s

fmtdec = lambda n, w : ("%0" + str(w) + "d") % n

fmt = FMT_DEC
formatter = fmtdec
count = 1
width = 0
mn = 0
mx = 255
sep = " "
for k, v in optlist:
    if k == '-c':
        try:
            count = int(v, 0)
        except ValueError, e:
            sys.stderr.write("%s: Error: Invalid parameter for option '%s'.\n" % (sys.argv[0], k))
            sys.exit(errno.EINVAL)
    if k == '-w':
        try:
            width = int(v, 0)
        except ValueError, e:
            sys.stderr.write("%s: Error: Invalid parameter for option '%s'.\n" % (sys.argv[0], k))
            sys.exit(errno.EINVAL)
    elif k == '-s':
        sep = v
    elif k == '-k':
        sep = "\n"
    elif k == '-d':
        fmt = FMT_DEC
        formatter = fmtdec
    elif k == '-h':
        fmt = FMT_HEX
        formatter = lambda n, w : ("%0" + str(w) + "x") % n
    elif k == '-o':
        fmt = FMT_OCT
        formatter = lambda n, w : ("%0" + str(w) + "o") % n
    elif k == '-b':
        fmt = FMT_BIN
        formatter = fmtbin
    elif k == '-6':
        fmt = FMT_B64
    elif k == '-X':
        try:
            mx = int(v, 0)
        except ValueError, e:
            sys.stderr.write("%s: Error: Invalid parameter for option '%s'.\n" % (sys.argv[0], k))
            sys.exit(errno.EINVAL)
    elif k == '-N':
        try:
            mn = int(v, 0)
        except ValueError, e:
            sys.stderr.write("%s: Error: Invalid parameter for option '%s'.\n" % (sys.argv[0], k))
            sys.exit(errno.EINVAL)
    elif k in ("-?", "--help"):
        print "rand - 1.0.0 - 2012 April 09"
        print "Brian Mearns <bmearns@ieee.org>"
        print ""
        print "Usage: %s [options]" % sys.argv[0]
        print ""
        print "Options:"
        print " -c COUNT        Specify the number of random values to output. (Default is 1)."
        print " -w WIDTH        Specify the minimum number of characters to output for each"
        print "                 element. (Elements with fewer characters will be 0 padded on"
        print "                 the left)."
        print " -d              Specify decimal for the output encoding. (Default)."
        print " -h              Specify hexidecimal for the output encoding."
        print " -o              Specify octal for the output encoding."
        print " -b              Specify binary for the output encoding."
        print " -6              Specify base-64 for the output encoding."
        print " -X MAX          Secify the maximum value for each element. (Default is 255)."
        print " -N MAX          Secify the minimum value for each element. (Default is 0)."
        print " -s SEP          Secify the separator string to use between elements. (Default"
        print "                 is single space)."
        print " -k              Use a linebreak as the separator between elements."
        print ""
        print "Misc:"
        print " -?, --help      Show this help message and exit."
        print ""
        print "Base-64 encoding (specified with the -6 option) is a special case: the MIN,"
        print "MAX, and SEP are all ignored. In this case, the specified COUNT of random bytes"
        print "is generated as a string and encoded together as base-64."
        print ""
        sys.exit(0)


rand = random.SystemRandom()
if fmt == FMT_B64:
    print base64.b64encode("".join(chr(rand.randint(0, 255)) for i in xrange(count)))
else:
    print sep.join(formatter(rand.randint(mn, mx), width) for i in xrange(count))


