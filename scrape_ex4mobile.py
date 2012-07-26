#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
from generate import Generate, RTTTLError


soup = BeautifulSoup(urllib2.urlopen('http://ez4mobile.com/nokiatone/rtttf.htm'))

for row in soup('font', {'color': '#000080'}):
    try:
        Generate(row.text)
    except RTTTLError:
        print "Could not convert {0}".format(row.text)
        continue
