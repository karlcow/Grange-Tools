#!/usr/bin/env python
# encoding: utf-8
"""
grenier_convert.py

Created by Karl Dubost on 2015-10-21.
Copyright (c) 2015 La Grange. All rights reserved.
MIT License
"""

import sys

import urllib


def fetch_note(uri):
    '''Fetch a note file and return the content.'''
    file_content = urllib.urlopen(uri)
    content = file_content.read()
    return content


def main():
    '''core program'''
    URI = 'file:tests/notes.md'
    # Fetch the content with a URI
    content = fetch_note(URI)
    # Parse the content
    # Convert in the format of your choice
    # Return the data

if __name__ == "__main__":
    sys.exit(main())
