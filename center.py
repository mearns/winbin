import sys, errno

def error(msg):
    sys.stderr.write("%s: Error: %s\n" % (sys.argv[0], msg))

def printVersion():
    print "%s - 1.0.0 2010 Sept 2" % sys.argv[0]

def printUsage():
    print "Usage: %s [-f] [-c CHAR] [-q] [-w] WIDTH <INPUT >OUPUT" % sys.argv[0]
    print "   or: %s [-f] [-c CHAR] [-p PADDING] [-a] <INPUT >OUTPUT" % sys.argv[0]

def printHelp():
    printVersion()
    print ""
    printUsage()
    print ""
    print "Center-align lines of text read from standard input, write to standard output."
    print "In the first form, specify the width to use for each line. In the second form,"
    print "Define the width dynamically based on the longest line, with optional padding."
    print ""
    print "Options:"
    print "  -w, --width WIDTH      Specify the width of the column to align the text in."
    print "                         WIDTH is specified in characters."
    print ""
    print "  -f, --fill             Indicates that the right side of lines should be"
    print "                         filled to the correct width, so that all lines are"
    print "                         exactly the same length."
    print ""
    print "  -a, --auto             Specifies that the width to use should be determined"
    print "                         automatically in order to fit the longest line,"
    print "                         including any padding (see --pad)."
    print ""
    print "  -p, --pad PADDING      Used with the --auto option, this indicates the"
    print "                         number of additional characters that will be added to"
    print "                         each side of the longest line in determining the"
    print "                         width."
    print ""
    print "  -c, --char CHAR        Specifes an alternate character to use for spacing."
    print "                         The default character is a space character (ASCII"
    print "                         value 0x20)."
    print ""
    print "  -q, --quiet            Used with the --width option, this suppresses errors"
    print "                         caused by lines that exceed the maximum width."
    print ""
    print "Misc:"
    print "  -h, -?, --help         Show this help message, then exit."
    print ""
    print "  -V, --version          Show the program version."
    print ""
    print "  --usage                Show a brief help message."
    print ""
    print "Lines read from standard input are prepended with the spacing character (a"
    print "space character by default, or the character specified with the --char option)"
    print "as necessary to center-align them in the configured width. If the --pad option"
    print "is given, then they right side of the line is likewise filled with the spacing"
    print "character. Lines that cannot be exactly center aligned are biased to the left."
    print ""
    print "In fixed-width mode (i.e., when a WIDTH is specified), lines that are too long"
    print "cause an error message to be printed to STDERR and the program terminates with"
    print "a non-zero error code (with partial output having been written). If the"
    print "--quiet option is given, long lines are simply printed as is (i.e., with no"
    print "alignment) and no error message is generated."
    print ""

width = None
char = ' '
fill = False
padding = 0
quiet = False

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg in ("--help", "-h", "-?", "/?", "/help"):
        printHelp()
        sys.exit(0)

    elif arg in ("--usage"):
        printUsage()
        sys.exit(0)

    elif arg in ("--version", "-V"):
        printVersion()
        sys.exit(0)

    elif arg in ("--width", "-w"):
        if i+1 < len(sys.argv):
            try:
                width = int(sys.argv[i+1])
            except ValueError, e:
                error(
                    "Bad value given for the \"%s\" option. WIDTH must be a decimal integer, not \"%s\"."
                    % (arg, sys.argv[i+1])
                )
                sys.exit(errno.EINVAL)
            i+=1
        else:
            error("The \"%s\" option requires a parameter. See --help for help." % arg)
            sys.exit(errno.EINVAL)

    elif arg in ("--fill", "-f"):
        fill = True

    elif arg in ("--auto", "-a"):
        width = None

    elif arg in ("--pad", "--padding", "-p"):
        if i+1 < len(sys.argv):
            try:
                padding = int(sys.argv[i+1])
                i+=1
            except ValueError, e:
                error(
                    "Bad value given for the \"%s\" option. PADDING must be a decimal integer, not \"%s\"."
                    % (arg, sys.argv[i+1])
                )
                sys.exit(errno.EINVAL)
        else:
            error("The \"%s\" option requires a parameter. See --help for help." % arg)
            sys.exit(errno.EINVAL)

    elif arg in ("--char", "-c"):
        if i+1 < len(sys.argv):
            char = sys.argv[i+1]
            if len(char) != 1:
                error(
                    "Bad value given for the \"%s\" option. CHAR must be a single character, not \"%s\"."
                    % (arg, char)
                )
                sys.exit(errno.EINVAL)
            i+=1
        else:
            error("The \"%s\" option requires a parameter. See --help for help." % arg)
            sys.exit(errno.EINVAL)

    elif arg in ("--quiet", "-q"):
        quiet = True

    else:
        try:
            width = int(arg)
        except ValueError, e:
            error(
                "Bad value given for the WIDTH argument. WIDTH must be a decimal integer, not \"%s\"."
                % (arg)
            )
            sys.exit(errno.EINVAL)

    i+=1
    
#For auto, pre-read all lines
if width is None:
    lines = []
    width = 0
    for line in sys.stdin:
        line = line.strip()
        lines.append(line)
        length = len(line)
        if length > width:
            width = length
    width += padding + padding
else:
    lines = sys.stdin

ln = 0
for line in lines:
    ln += 1
    line = line.strip()
    delta = width - len(line)
    left = 0
    right = 0
    if delta < 0 and not quiet:
        error("Line #%d is too long. Width is %d, line is %d chars long." % (ln, width, len(line)))
        sys.exit(errno.EINVAL)
    elif delta > 0:
        left = int(delta / 2)
        if fill:
            right = delta - left

    print "".join(char for i in range(left)) + line + "".join(char for i in range(right))

