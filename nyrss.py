#!/usr/bin/env python

# Usage: nyrss.py horriblesubs "blame 720p" 24

import xml.etree.ElementTree as ET
import sys
import urllib2

from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print 'Too few parameters!'
        exit(1)
    elif len(sys.argv) == 3:
        SEARCH_USER = sys.argv[1]
        SEARCH_QUERY = sys.argv[2]
        MAX_AGE = None
    elif len(sys.argv) == 4:
        SEARCH_USER = sys.argv[1]
        SEARCH_QUERY = sys.argv[2]
        MAX_AGE = int(sys.argv[3])
    else:
        print 'Too many parameters!'
        exit(1)

    rss_response = urllib2.urlopen('https://nyaa.si/?page=rss&q=%s&c=0_0&f=0&u=%s' % (SEARCH_QUERY, SEARCH_USER))
    rss = rss_response.read()
    root = ET.fromstring(rss)
    
    items = root.findall('channel/item')

    for item in items:
        title = item.findall('title')[0].text
        link =  urllib2.unquote(item.findall('link')[0].text)
        pubDate = datetime.strptime(item.findall('pubDate')[0].text[:-6], '%a, %d %b %Y %H:%M:%S') # Time zone is ignored
        delta = datetime.utcnow() - pubDate # Uses UTC time zone
        age = delta.days * 24 + delta.seconds / 3600.0 # Age in hours
        
        if MAX_AGE is not None and MAX_AGE < age:
            continue
        
        print title
        print link
        print pubDate
        print age
        print
        
        torrent_response = urllib2.urlopen(link)
        torrent = torrent_response.read()
        f = open(title + '.torrent', 'wb')
        f.write(torrent)
        f.close()
