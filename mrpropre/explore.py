#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Explore La Grange.

* Create a list of all files.'''

import os
import requests
from lxml import etree
import StringIO

ROOTDIR = '/Users/karl/Sites/la-grange.net'
DIREXPLORE = '/Users/karl/Sites/la-grange.net/'
DOMAIN = 'http://www.la-grange.net'


def find_filepaths(ROOTDIR):
    '''Returns a list of file paths.'''
    filepaths_list = []
    for dirpath, dirnames, files in os.walk(ROOTDIR):
        for name in files:
            if name.lower().endswith('html') or name.lower().endswith('xhtml'):
                filepaths_list.append(os.path.join(dirpath, name))
    return filepaths_list


def http_encoding(response):
    '''returns the HTTP encoding value.'''
    return response.encoding


def extract_meta_charset(content):
    '''extracts the meta charset from the html.'''
    # HTML5 charset path
    html5_path = "//meta/@charset"
    # HTML http-equiv needs to take care the different content-type case
    regexpNS = "http://exslt.org/regular-expressions"
    http_equiv_find = etree.XPath(
        "//meta[re:test(@http-equiv,'content-type', 'i')]/@content",
        namespaces={'re': regexpNS})
    parser = etree.HTMLParser()
    root = etree.parse(StringIO.StringIO(content), parser)
    if root.xpath(html5_path):
        meta_charset = root.xpath(html5_path)[0]
    elif http_equiv_find(root):
        content_type = http_equiv_find(root)[0]
        # sometimes content-type will not contain a charset
        try:
            meta_charset = content_type.split('=')[1]
        except Exception:
            meta_charset = None
    else:
        meta_charset = None
    return meta_charset

if __name__ == '__main__':
    print('-' * 80)
    print('Mr Propre - Analysis of La Grange')
    print('-' * 80)
    filepaths_list = find_filepaths(DIREXPLORE)
    print('{0} files to analyze'.format(len(filepaths_list)))
    print('-' * 80)
    with open('charset.log', 'a') as flog:
        for path in filepaths_list:
            content = None
            url = path.replace(ROOTDIR, DOMAIN)
            r = requests.head(url)
            status_code = r.status_code
            # Avoids private documents
            if status_code == 200:
                print "# {}".format(path)
                with open(path, 'r') as f:
                    content = f.read()
                # Only not empty content (even white space)
                if content.strip():
                    meta_charset = extract_meta_charset(content)
                    http_charset = http_encoding(r)
                    if http_charset != meta_charset:
                        flog.write('{} {} {}\n'.format(
                            http_charset, meta_charset, url))
                        # print http_charset, meta_charset, url
