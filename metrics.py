#! /usr/bin/env python
# -*- coding: utf-8 -*-


from metricparser import connector, result


def main():
    f = open('seed.txt', 'rb+')
    urls = f.readlines()

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
            unique.append(url.replace('\n', ''))
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

    find = raw_input('Begin search for urls in %s? (y/n): ' % f.name)
    if find == 'y':
        num_urls = int(raw_input('Number of urls: '))
        if num_urls:
            url_finder(urls, result, num_urls)

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

    search = raw_input('Search for metrics code in %s? (y/n): ' % result)
    if search == 'y':
        metric = int(raw_input('Mixpanel/Kissmetrics?(1/2): '))
        if metric == 1:
            source = 'mixpanel'
        elif metric == 2:
            source = 'kissmetrics'
        try:
            main_script(fixed_list, source=source)
        except Exception as e:
            print e
    else:
        exit()

