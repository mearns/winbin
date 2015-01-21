#! /usr/bin/env python
# vim: set fileencoding=utf-8: 
""" Process URL for intersphinx targets and emit html or text """

def validuri(string):
   return string

from sphinx.ext.intersphinx import read_inventory_v2
from posixpath import join
import pprint
import argparse
import locale
import os,sys
import urllib2
from cStringIO import StringIO


parser = argparse.ArgumentParser(description='Process intersphinx link library')

parser.add_argument('--url' , type=validuri, help="URL to retrieve objects.inv from")
parser.add_argument('--file' , help="objects.inv format file")
parser.add_argument('--output' , help="Output file to write to (defaults to stdout)")

group = parser.add_mutually_exclusive_group(required=False)

group.add_argument('--html', action='store_true', help="Output HTML")
group.add_argument('--terse', action='store_true', help="Output terse text list")
group.add_argument('--rst', action='store_true', help="Output ReStructuredText")
group.add_argument('--rewrite', action='store_true', help="Output short form and correct form of each link.")


args = parser.parse_args()

def start_role(role):
    if (args.terse):
        return
    elif (args.rewrite):
        return
    elif (args.rst):
        print role
    else:
        print "<dt>Role: {}</dt>\n<dd>\n<dl>\n".format(role)

def start_item(role,item):
    if (args.terse):
        return
    elif (args.rewrite):
        return
    elif (args.rst):
        print "\t:{}:{}:".format(role,item)
    elif (args.html):
        print "<dt>{}:{}</dt>\n".format(role,item)
        print "<dd>"
        print "<table>\n<tbody>"
        
def end_item(role,item):
    if (args.html):
        print "</tbody></table>"
        print "</dd>\n"

def print_link(role,item,domain,title):
    """Return the correct link form, if no title then extended form."""

    domain = domain.lower()
    if (title == '')|(title=='-'):
        linkStr = ":{}:`{} <{}:{}>`".format(role,item,domain,item)
    else:
        linkStr = ":{}:`{}:{}`".format(role,domain,item)
    
    if (args.terse):
        print linkStr
    if (args.rewrite):
        print ":{}:`{}:{}`".format(role,domain,item), "\t{}".format(linkStr)
    elif (args.rst):
        print "\t\t:Link:\t{}".format(linkStr)
    elif (args.html):
        print "<tr><th>Link:</th><td>{}</td></tr>".format(linkStr)      

def end_role():
    if (args.html):
        print "</dl>\n"
        print "</dd>\n"
        
def print_meta(role,item,domain,version,url,title):
    if (args.terse):
        return
    elif (args.rewrite):
        return
    elif (args.rst):
        print "\t\t:Domain:\t{}".format(domain)
        print "\t\t:Version:\t{}".format(version)
        print "\t\t:URL:\t{}".format(url)
        print "\t\t:Title:\t{}".format(title)
    elif (args.html):
        print "<tr><th>Domain:</th><td>{}</td></tr>".format(domain)
        print "<tr><th>Version:</th><td>{}</td></tr>".format(version)
        print "<tr><th>URL:</th><td>{}</td></tr>".format(url)
        print "<tr><th>Title:</th><td>{}</td></tr>".format(title)
    return

def fetch_data(url,f):

    line = f.readline() # burn a line
    invdata = read_inventory_v2(f, url or '', join)
    if (args.html):
        print "<dl>"
    for role in invdata:
        start_role(role)
        for item in invdata[role]:
            (domain, version, url, title) = invdata[role][item]
            #sys.stderr.write("{}:{} :: {}\n".format(role,item,invdata[role][item]))
            start_item(role,item)
            print_link(role,item,domain,title)
            print_meta(role,item,domain,version,url,title)
            end_item(role,item)
        if (args.html):
            print "</dl>\n"
    
if __name__ == "__main__":

    import errno

    if (args.file):
        inv = args.file
#       if os.path.exists(inv) == False:
#           raise Exception('File "{}" does not exist'.format(inv))
    else:
        inv = False
    if (args.url):
        url = args.url          
    else:
        url = False

    if args.output:
        sys.stdout = open(args.output, "wb")
        
    
    # sys.stderr.write('URL({}) FN({})\n'.format(url,fn))
        
    if (inv == False) & (url == False):
        print >> sys.stderr, "Need to specify either a file or a URL."
        parser.print_usage(sys.stderr)
        sys.exit(errno.EINVAL)
   
    if (inv != False ) & (url != ''):
        #sys.stderr.write("Reading from: {}\n".format(inv))
        #sys.stderr.write("Using: {} as base HREF\n".format(url))
        with open(inv, 'rb') as f:
            fetch_data(url, f)
    elif (url != False):
        # fetch URL into inv
        #sys.stderr.write("Retrieving objects.inv from {}\n".format(url))
        if (url.rfind('objects.inv')>5):
            invdata = urllib2.urlopen(url)
        else:
            invdata = urllib2.urlopen(url + '/objects.inv')
        sys.stderr.write('URL resolved to: {}\n '.format(invdata.geturl()))
        #print invdata.read()
        f = StringIO(invdata.read())
        sys.stderr.write("Using: {} as base HREF\n".format(url))
        fetch_data(url,f)
    else:
        raise Exception("You need to specify a --URL")

