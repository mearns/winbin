#! /usr/bin/env python
# vim: set fileencoding=utf-8: set encoding=utf-8:

import time
import sys
import subprocess
import os
import errno
import re
from StringIO import StringIO

PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]
VER_MAJOR = 1
VER_MINOR = 0
VER_PATCH = 0
VER_SEMANTIC = 0

def timer(count, command_args, nooutput=False):
    if len(command_args) == 0:
        return 0, 0.0

    r = range(count)
    codes = [0]*count
    if nooutput:
        buff = open(os.devnull, "w")
        start = time.time()
        for i in r:
            codes[i] = subprocess.call(command_args, stderr=subprocess.STDOUT, stdout=buff)
        stop = time.time()
    else:
        start = time.time()
        for i in r:
            codes[i] = subprocess.call(command_args)
        stop = time.time()

    seconds = stop - start
    codes = filter(lambda x : x != 0, codes)
    if codes:
        exitcode = codes[-1]
    else:
        exitcode = 0
    return exitcode, seconds / float(count)

def format_time(seconds):

    mins, seconds = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    output = ""
    if weeks:
        output += "%d w " % weeks
    if hours:
        output += "%d d " % days
    if mins:
        output += "%d m " % mins
    output += "%.3f s" % seconds

    return output

def default_args(args, prog_name):
    if args is None:
        args = sys.argv[1:]
        if prog_name is None:
            prog_name = os.path.basename(sys.argv[0])
    else:
        if prog_name is None:
            prog_name = PROG_NAME

    return args, prog_name
    
def show_help(prog_name):
    sys.stdout.write('''%(PROG_NAME)s v%(VERSION)s

Usage:  %(PROG_NAME)s [options] [--] [COMMAND [CMD_ARGS [...]]]
   or:  %(PROG_NAME)s --help

Execute the specified COMMAND with the specified CMD_ARGS one or more times
and report the average runtime for the command.

Options:

 -c COUNT                   Execute the given command COUNT number of times.
                            The default count is 1. Can also be written as
                            -1, -2, -3, ... to execute 1, 2, 3, ... times.

 -s                         Supress STDOUT and STDERR output from the executed
                            command.

 --help                     Show this help information.


This program times how long it takes itself to execute the specified COMMAND
with the specified CMD_ARGS as arguments, the specified number of times (1 by
default, COUNT if the -c or equivalent option is given). This includes some
very minimal base overhead in this program itself, as well as some small
overhead for each execution (e.g., opening a sub process to run the command
in).

The total time is divided by the number of executions (e.g., COUNT) to get the
average time, which is reported to STDOUT in a human friendly way.

The "exit code" for the executed command is also reported, and is used as the
exit code for this process. Since the command may be run multiple times, it
could conceivably produce different exit codes: the one that is used is the 
last non-zero code returned, or 0 if they all returned 0.
''' % dict(
        PROG_NAME = prog_name,
        VERSION = '.'.join(str(v) for v in (VER_MAJOR, VER_MINOR, VER_PATCH, VER_SEMANTIC)),
    ))

class InvalidArgumentError(Exception): pass

_number_match = re.compile(r'-(\d+)')

def parse_args(args, prog_name):

    #Default options
    count = 1
    nooutput = False

    while args:
        arg = args.pop(0)
        if arg[0] == '-':
            if arg == '--':
                break
            elif arg == '-c':
                try:
                    count = args.pop(0)
                except IndexError:
                    raise InvalidArgumentError('Missing required parameter for -c option.')

                try:
                    count = int(count)
                except ValueError:
                    raise InvalidArgumentError('Invalid parameter for -c option: expected an integer: %s' % (count,))

            elif arg == '-s':
                nooutput = True

            elif arg in ('-h', '-?', '--help'):
                show_help(prog_name)
                return None, None, True

            else:
                mobj = _number_match.match(arg)
                if mobj:
                    count = int(mobj.group(1))
                else:
                    raise InvalidArgumentError('Unknown option: %s' % (arg,))

        elif arg.lower() in ('/?', '/help'):
            show_help(prog_name)
            return None, None, True

        else:
            args.insert(0, arg)
            break

    return args, dict(
        count = count,
        nooutput = nooutput,
    ), False



def main(args=None, prog_name = None):

    args, prog_name = default_args(args, prog_name)

    try:
        args, opts, exit = parse_args(args, prog_name)
    except InvalidArgumentError, e:
        sys.stderr.write('%s: Error: %s\n' % (prog_name, e))
        return errno.EINVAL

    if exit:
        return 0

    exitcode, seconds = timer(opts['count'], args, opts['nooutput'])
    print '---------------'
    if exitcode != 0:
        print "Exited with code %d" % exitcode
    print "Average runtime: %s" % (format_time(seconds),)
    return exitcode

if __name__ == '__main__':
    sys.exit(main())


