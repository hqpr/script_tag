#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from metricparser import connector, result


def main():
    DEBUG = True
    if DEBUG:
        # urls = ['urls/qa.html', 'urls/cb.html', 'urls/m1.html', 'urls/m2.html', 'urls/k1.html', 'urls/k2.html']
        f = open('seed.txt', 'rb+')
        urls = f.readlines()
    else:
        urls = ['http://bing.com/', ]

    def saving_scripts(name, what_to_save, flag):
        """
        Saves all script tags to txt files
        Not in use so far
        """
        filename = '%s_%s.txt' % (name[7:], flag)
        fp = open(filename, 'ab+')
        fp.write(str(what_to_save))

    def url_finder(seed, result_file, max_number_of_distinct_urls=None):
        l = open(result_file, 'wb+')
        unique = []
        for url in seed:
            unique.append(url)
            print '%s [saved]' % url
            for links in connector(url)('a')[:max_number_of_distinct_urls]:
                if links.get('href') and links.get('href') != 'None':
                    link = links.get('href')
                    if str(link).startswith('http'):  # only external links
                        domain = 'http://' + str(link).split('/')[2]  # only base domain
                        if url != domain:  # only unique urls
                            if domain not in unique:
                                unique.append(domain)
                                print '%s [saved]' % domain
        for u in unique:
            l.write(u + '\n')

    url_finder(urls, result, 1)

if __name__ == "__main__":
    main()
    from metricparser import main_script
    fr = open(result, 'rb+')
    grabed_urls = fr.readlines()

    # Strange error with \n
    fixed_list = []
    for x in grabed_urls:
        if x != '\n':
            fixed_list.append(x.replace('\n', ''))
    try:
        main_script(fixed_list, source='mixpanel')
    except Exception as e:
        print e

