#! /usr/bin/env python
# vim: set fileencoding=utf-8: 

def generate_batch_file(script):
        command = None
        base, ext = os.path.splitext(script)
        ext = ext.lower()
        if ext in (".py", ".pyc", ".pyo", ".py3", ".pyw"):
            command = "python"
        elif ext in (".pl", ".pm", ".perl"):
            command = "perl"
        elif ext in (".exe", ".bat", ".cmd", ".com"):
            return None
            
        if command is None:
            raise Exception("Unrecognized file extension '%s'." % ext)

        ofile = base + ".bat"
        with open(ofile, "w") as ostream:
            ostream.write('@%s "%%~dp0.\\%s" %%*\n' % (command, script))

        return ofile

if __name__ == '__main__':

    import sys
    import os.path

    errors = 0
    for script in sys.argv[1:]:
        try:
            generated = generate_batch_file(script)
        except Exception, e:
            errors += 1
            sys.stderr.write("Error generating batch script for %r:\n%s\n" % (script, e))
        else:
            if generated is None:
                print "File is already executable: %s" % script
            else:
                print "Generated: %s" % generated
            

            

