import sys
import errno

buffered = True
padding = 1
tabsize = 4
separators = []

officialName = "columns"
version = "1.1.0"
date = "2012 June 26"
programName = sys.argv[0]

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    i=i+1

    if arg == "-b":
        buffered = True

    elif arg == "-B":
        buffered = False

    elif arg == "-S":
        separators = []

    elif arg == "-s":
        if i < len(sys.argv):
            val = sys.argv[i]
            i=i+1
            separators.append(val)

        else:
            sys.stderr.write("%s: Error: Missing parameter for '-s' option.\n" % programName)
            sys.exit(errno.EINVAL)
        
    elif arg == "-p":
        if i < len(sys.argv):
            val = sys.argv[i]
            i=i+1
            try:
                p = int(val)
            except ValueError, e:
                sys.stderr.write("%s: Error: Illegal parameter for '-p' option. Expected a decimal integer, not \"%s\".\n"
                    % (programName, val))
                sys.exit(errno.EINVAL)
            
            if p >= 0:
                padding = p
            else:
                sys.stderr.write("%s: Error: Illegal parameter value for '-p' option. Value is less than 0: %u\n"
                    % (programName, p))
                sys.exit(errno.EINVAL)

        else:
            sys.stderr.write("%s: Error: Missing parameter for '-p' option.\n" % programName)
            sys.exit(errno.EINVAL)

    elif arg == "-t":
        if i < len(sys.argv):
            val = sys.argv[i]
            i=i+1
            try:
                t = int(val)
            except ValueError, e:
                sys.stderr.write("%s: Error: Illegal parameter for '-t' option. Expected a decimal integer, not \"%s\".\n"
                    % (programName, val))
                sys.exit(errno.EINVAL)
            
            if t > 0:
                tabsize = t;
            else:
                sys.stderr.write("%s: Error: Illegal parameter value for '-t' option. Value is not greater than 0: %u\n"
                    % (programName, t))
                sys.exit(errno.EINVAL)
        else:
            sys.stderr.write("%s: Error: Missing parameter for '-t' option.\n" % programName)
            sys.exit(errno.EINVAL)

    elif arg == "-h" or arg == "-?" or arg == "--help":
        sys.stdout.write(
"""{name} - {version} {date}

Usage: {invName} [options] < INPUT_FILE > OUTPUT_FILE

Format text based data in INPUT_FILE into columns. Each line is split into
fields at whitespace delimiters, and the fields are arranged into columns
with a more consistent amount of whitespace between them.

Options:
 -p PADDING         (default = 1) Minimum number of "tabs" seperating each
                    column in the output.

 -t TABSIZE         (default = 4) The size of a "tab". Output is generated
                    assuming there is a tab stop ever TABSIZE characters.

 -b                 (default) Use buffering for maximum prettiness. This
                    allows the columns to be formatted taking into account
                    every row, but requires the entire contents of
                    INPUT_FILE to be loaded into 

 -B                 Do not use buffering. Each line is formatted based on
                    the current and preceeding lines only, so spacing may
                    change throughout the document, but it does not require
                    much memory.

Misc. Options:
  -h, -?, --help    Print this help message to STDOUT and exit without
                    error.
""".format(
            name = officialName,
            version = version,
            date = date,
            invName = programName
        ))
        sys.exit(0)

    else:
        sys.stderr.write("%s: Error: Unknown argument, try --help: %s\n" % (programName, arg))
        sys.exit(errno.EINVAL)


lines = []
maxFieldWidths = []

for line in sys.stdin:
    if len(separators) == 0:
        fields = line.split()
    else:
        #FIXME: This isn't working right.
        fields = []
        line = line.strip()
        while len(line) > 0:
            which = None
            where = len(line)
            for i in xrange(len(separators)):
                idx = line.find(separators[i])
                if idx < where:
                    where = idx
                    which = i
            if which is None:
                fields.append(line)
                line = ""
            else:
                where += len(separators[which])
                newField = line[:where].strip()
                fields.append(newField)
                line = line[where:].strip()

    if buffered:
        lines.append(fields)

    linePos = 0
    for i in range(len(fields)):
        #No data for this field yet...
        if i >= len(maxFieldWidths):
            maxFieldWidths.append(len(fields[i]))
        elif maxFieldWidths[i] < len(fields[i]):
            maxFieldWidths[i] = len(fields[i])

        if not buffered:
            #Find the end of the longest field
            endOfField = linePos + maxFieldWidths[i]
            #Out to the next tabstop
            if (endOfField % tabsize) != 0:
                endOfField = tabsize * (int(endOfField / tabsize) + 1)
            else:
                endOfField = tabsize * (int(endOfField / tabsize))
            endOfField += tabsize * padding

            #Write the field value.
            sys.stdout.write(fields[i])

            #Pad to the next field.
            paddStr = ""
            linePos += len(fields[i])
            while linePos < endOfField:
                paddStr += " "
                linePos += 1
            sys.stdout.write(paddStr)

    if not buffered:
        sys.stdout.write("\n")
            


if buffered:
    for fields in lines:
        linePos = 0
        for i in range(len(fields)):
            #Find the end of the longest field
            endOfField = linePos + maxFieldWidths[i]
            #Out to the next tabstop
            if (endOfField % tabsize) != 0:
                endOfField = tabsize * (int(endOfField / tabsize) + 1)
            else:
                endOfField = tabsize * (int(endOfField / tabsize))
            endOfField += tabsize * padding

            #Write the field value.
            sys.stdout.write(fields[i])

            #Pad to the next field.
            if i+1 < len(fields):
                paddStr = ""
                linePos += len(fields[i])
                while linePos < endOfField:
                    paddStr += " "
                    linePos += 1
                sys.stdout.write(paddStr)

        sys.stdout.write("\n")

sys.exit(0)

