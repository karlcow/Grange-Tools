#!/usr/bin/env python3
# encoding: utf-8
"""
firstpixel.py

Created by Karl Dubost on 2017-01-17.
Copyright (c) 2017 La Grange. All rights reserved.
MIT License
"""

import argparse
import os
import sys


def read_pixel(image):
    pass


def parse_cli():
    '''Returns CLI arguments.'''
    parser = argparse.ArgumentParser(
        description='Read the first pixel of images.')
    parser.add_argument('directory', metavar='d',
                        help='a directory with images')
    args = parser.parse_args()
    return args.file


def main():
    '''core program'''
    filepath = parse_cli()
    if os.path.isfile(filepath):
        uri = 'file://{0}'.format(os.path.realpath(filepath))
    else:
        sys.exit('Wrong filename: {0}'.format(filepath))
    pass


if __name__ == "__main__":
    sys.exit(main())
