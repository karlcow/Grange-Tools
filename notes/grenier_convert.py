#!/usr/bin/env python3
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
import os.path
import sys
import urllib.request

Note = namedtuple('Note', 'note_type, prose, link, quote')

ARTICLE_TEMPLATE = '<article class="{type}" id={id}>{html}</article>'
PROSE_TEMPLATE = '''<p>{prose}</p>'''
QUOTE_TEMPLATE = '''<p>{prose} <q cite='{uri}'>{quote_text}</q></p>'''

INTRO = '''

Converting notes located at
{0}

'''


def fetch_note(uri):
    '''Fetches a note file and return the content.'''
    with urllib.request.urlopen(uri) as f:
        content = f.read().decode('utf-8')
    return content


def parse_notes(content):
    '''Parses a note and sends back a data structure.'''
    notes_list = []
    for note in content.split('---'):
        if note.strip():
            prose = ''
            link = ''
            quote = ''
            note_type = 'prose'
            for line in note.splitlines():
                if line.startswith('>'):
                    note_type = 'quote'
                    quote = line
                if line.startswith('http'):
                    if not note_type == 'quote':
                        note_type = 'link'
                    link = line
                if note_type == 'prose':
                    prose += '{} '.format(line)
            notes_list.append(Note(note_type, prose, link, quote))
        else:
            print('Invalid: empty note')
    return notes_list


def format_note(note):
    '''Returns the HTML markup for a note.'''
    html_note = ''
    note_id = link_id(note.prose)
    if note.note_type == 'prose' or note.note_type == 'link':
        prose = format_link(note.prose, note.link).strip()
        html_note = PROSE_TEMPLATE.format(prose=prose)
    if note.note_type == 'quote':
        prose = format_link(note.prose, note.link)
        html_note = QUOTE_TEMPLATE.format(
            prose=prose, uri=note.link, quote_text=note.quote[1:].strip())
    html_note = ARTICLE_TEMPLATE.format(
        type=note.note_type, id=note_id, html=html_note)
    return html_note


def link_id(text):
    '''Retuns an id for the markup.'''
    text = text.encode('utf-8')
    return 'id{0}'.format(hashlib.sha1(text).hexdigest()[:10])


def format_link(comment, uri):
    '''Returns a linkified text.'''
    a_start = "<a href='{uri}'>".format(uri=uri)
    if ('[' and ']') in comment:
        comment = comment.replace('[', a_start)
        comment = comment.replace(']', '</a>')
    return comment


def parse_cli():
    '''Returns CLI arguments.'''
    parser = argparse.ArgumentParser(description='Convert notes in markup.')
    parser.add_argument('file', metavar='f', help='a filepath')
    args = parser.parse_args()
    return args.file


def main():
    '''core program'''
    grenier = ''
    filepath = parse_cli()
    if os.path.isfile(filepath):
        uri = 'file://{0}'.format(os.path.realpath(filepath))
    else:
        sys.exit('Wrong filename: {0}'.format(filepath))
    print(INTRO.format(uri))
    # Fetch the content with a URI
    print('Fetching: {0}'.format(uri))
    content = fetch_note(uri)
    # Parse the content
    print('Parsing:  {0}'.format(uri))
    notes_list = parse_notes(content)
    print('Formatting notes')
    for note in notes_list:
        grenier += '{}\n\n'.format(format_note(note))
    return grenier


if __name__ == "__main__":
    sys.exit(main())
