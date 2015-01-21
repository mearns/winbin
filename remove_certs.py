from _winreg import *
import sys

total_found = 0
total_removed = 0
success = True

keys = (
    (HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r'SOFTWARE\Policies\Microsoft\SystemCertificates\Root\Certificates'),
    (HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r'SOFTWARE\Policies\Microsoft\SystemCertificates\CA\Certificates'),
    (HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r'SOFTWARE\Microsoft\SystemCertificates\ROOT\Certificates'),
    (HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", r'SOFTWARE\Microsoft\SystemCertificates\CA\Certificates'),
)
for root, root_name, key_name in keys:
    key = OpenKey(HKEY_LOCAL_MACHINE, key_name)
    to_remove = []
    try:
        i = 0
        while True:
            subkey_name = EnumKey(key, i)
            subkey = OpenKey(key, subkey_name)
            blob = QueryValueEx(subkey, "Blob")
            CloseKey(subkey)
            if blob[0].lower().find("zscaler") != -1:
                to_remove.append(subkey_name)
                total_found += 1
            i += 1
    except WindowsError:
        #Done enumerating
        pass

    for subkey_name in to_remove:
        try:
            DeleteKey(key, subkey_name)
            total_removed += 1
        except WindowsError, e:
            success = False
            sys.stderr.write("Error: Failed to delete registry key: '%s\%s\%s'\n" % (root_name, key_name, subkey_name))
            sys.stderr.write(str(e) + "\n\n")


print "Found %d keys." % total_found
print "Removed %d keys." % total_removed
if success and (total_found == total_removed):
    print "Success!"
    sys.exit(0)
else:
    print "FAILED!"
    sys.exit(1)

