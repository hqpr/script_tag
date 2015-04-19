#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
from bs4 import BeautifulSoup

DEBUG = True

if DEBUG:
    urls = ['urls/debug.html']
else:
    urls = ['urls/cb.html', 'urls/tc.html', 'urls/tm.html']


def connector(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup


def dive_in(url):
    for link in connector(url)('a'):
        print link


def script_grab(url):
    for script in connector(url)(["script"]):
        filename = '%s.txt' % url[7:]
        fp = open(filename, 'wb+')
        fp.write(str(script))


def url_finder(seed, max_number_of_distinct_urls, depth, unique=False):

    for url in seed:

        if unique:

            for links in connector(url)('a'):
                if links.get('href') and links.get('href') != 'None':
                    link = links.get('href')
                    if str(link).startswith('http'):
                        domain = 'http://' + str(link).split('/')[2]
                        print '[1] %s -> %s' % (url, domain)
                        script_grab(domain)

        else:
            d = {}
            for links in connector(url)('a'):

                if links.get('href') and links.get('href') != 'None':
                    link = links.get('href')
                    if str(link).startswith('http'):
                        d.update({url: []})
                        print '[1] %s -> %s' % (url, link)

                        for l in connector(link)('a')[:max_number_of_distinct_urls]:
                            l = l.get('href')
                            if str(l).startswith('http'):
                                print '[2] %s -> %s' % (url, l)
                                print
                                d[url].append(l)

            print 'ADDED: %s' % [len(v) for k, v in d.items()][0]


url_finder(urls, 500, 4, unique=True)

