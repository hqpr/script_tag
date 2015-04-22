#! /usr/bin/env python


import urllib
from bs4 import BeautifulSoup


result = 'results.txt'
try:
    fr = open(result, 'rb+')
except IOError:
    fr = open(result, 'wb+')


def connector(url):
    html = urllib.urlopen(url).read().replace('</html>', '')  # if script tags outside html doc
    soup = BeautifulSoup(html)
    return soup


def saving(what_to_save, source='asd'):
    """ Saves urls in source.txt file """
    filename = '%s.txt' % source
    fp = open(filename, 'ab+')
    fp.write(str(what_to_save+'\n'))


def main_script(seed, source):
    """ Search for metric name in html body """
    print
    print 'Searching for %s...' % source
    for url in seed:
        for script in connector(url)("script"):
            if str(script).__contains__(source):
                print '%s -> %s' % (url, source)
                saving(url, source)
