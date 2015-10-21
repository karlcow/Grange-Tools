#!/usr/bin/env python
# encoding: utf-8
"""
grenier_convert.py

Created by Karl Dubost on 2015-10-21.
Copyright (c) 2015 La Grange. All rights reserved.
MIT License
"""

import argparse
from collections import namedtuple
import hashlib
import sys
import urllib

Link = namedtuple('Link', 'link text quote')

LINK_TEMPLATE = '''<article>
<p id='{link_id}'>{text} {quote}</p>
</article>
'''

QUOTE_TEMPLATE = '''<q cite='{uri}'>{quote_text}</q>'''

INTRO = '''
---------------------------
Converting notes located at
{0}
---------------------------
'''


def fetch_note(uri):
    '''Fetches a note file and return the content.'''
    file_content = urllib.urlopen(uri)
    content = file_content.readlines()
    return content


def parse_note(content):
    '''Parses a note and sends back a data structure.'''
    grenier = []
    # There might not be a quote.
    quote = ''
    for line in content:
        line.strip()
        if not line.startswith('---'):
            if line.startswith('>'):
                # remove the first > character
                quote = line[1:].strip('\n')
            elif line.startswith('http'):
                link = line.strip('\n')
            else:
                if not line.startswith('\n'):
                    text = line.strip('\n')
        else:
            grenier.append(Link(link, text, quote))
    return grenier


def link_id(text):
    '''Retuns an id for the markup.'''
    return 'id{0}'.format(hashlib.sha1(text).hexdigest()[:10])


def format_link(comment, uri):
    '''Returns a linkified text.'''
    a_start = "<a href='{uri}'>".format(uri=uri)
    comment = comment.replace('[', a_start)
    comment = comment.replace(']', '</a>')
    return comment


def format_markup(link_data, template):
    '''Converts link_data to markup.'''
    QUOTE_FLAG = False
    uri = link_data.link
    quote_text = link_data.quote
    comment_markup = format_link(link_data.text, uri)
    if quote_text:
        QUOTE_FLAG = True
        quote = QUOTE_TEMPLATE.format(
            uri=uri,
            quote_text=quote_text)
    return LINK_TEMPLATE.format(
        link_id=link_id(link_data.text),
        text=comment_markup,
        quote=quote if QUOTE_FLAG else '')


def parse_cli():
    '''Returns CLI arguments.'''
    parser = argparse.ArgumentParser(description='Convert notes in markup.')
    parser.add_argument('file', metavar='f', type=file, help='a filepath')
    args = parser.parse_args()
    return args.file


def main():
    '''core program'''
    filename = parse_cli()
    URI = filename.name or 'file:tests/notes.md'
    print(INTRO.format(URI))
    # Fetch the content with a URI
    content = fetch_note(URI)
    # Parse the content
    grenier = parse_note(content)
    # Convert in the format of your choice
    # markup = ''
    for link_data in grenier:
        print format_markup(link_data, LINK_TEMPLATE)

    # Return the data

if __name__ == "__main__":
    sys.exit(main())
