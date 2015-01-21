import sys
import os.path
import errno

progname = os.path.basename(sys.argv[0])
VERS_MAJOR = 1
VERS_MINOR = 0
VERS_PATCH = 0

verbose = False
for arg in sys.argv[1:]:
    if arg in ("-v", "--verbose"):
        verbose = True

    elif arg in ("-h", "--help", "-?"):
        sys.stdout.write(
"""%(progname)s - %(ver)s

Usage: %(progname)s [-v]
   or: %(progname)s -h

Print a list of serial ports available on the system.

Options:
  -v, --verbose         Create verbose output, including descriptions of each
                        port that is found.
  -h, -?, --help        Show this help documentation.

This program requires the pyserial module, version 2.6 or later. See
<http://pyserial.sourceforge.net/>.

""" % {
    "progname": progname,
    "ver": ("%d.%d.%d" % (VERS_MAJOR, VERS_MINOR, VERS_PATCH)),
})
        sys.exit(0)

    else:
        sys.stderr.write("%s: Error: Unexpected argument '%s'. Try --help.\n" % (progname, arg))
        sys.exit(errno.EINVAL)

try:
    from serial.tools.list_ports import comports
except ImportError:
    sys.stderr.write("%s: Error: Could not import required pyserial module tools.list_ports.\n" % (progname))
    sys.stderr.write("    You may need to upgrade to the latest version of pyserial.\n")
    sys.exit(1)

for port, desc, hwid in sorted(comports()):
    if verbose:
        sys.stdout.write('-%-10s %s --- [%s]\n' % (port, desc, hwid))
    else:
        print port
        

