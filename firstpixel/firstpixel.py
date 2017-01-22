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
from PIL import Image
import sys

HTML_DIV = '<div style="height:50px;width:50px;{css_string}"> </div>'


def read_pixel(image_path):
    img = Image.open(image_path)
    img_data = img.load()
    # upper left corner of the image
    first_pixel = img_data[0, 0]
    return first_pixel


def images_list(directory):
    files_list = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            files_list.append(file_path)
    return files_list


def parse_cli():
    '''Returns CLI arguments.'''
    parser = argparse.ArgumentParser(
        description='Read the first pixel of images.')
    parser.add_argument('directory', metavar='d',
                        help='a directory with images')
    args = parser.parse_args()
    return args.directory


def main():
    '''core program'''
    directory = parse_cli()
    if os.path.isdir(directory):
        files_list = images_list(directory)
    else:
        sys.exit('Wrong directory: {0}'.format(directory))
    html = ''
    for image_path in files_list:
        r, g, b = read_pixel(image_path)
        css_string = 'background-color: rgb({r}, {g}, {b});'.format(
            r=r, g=g, b=b)
        html += HTML_DIV.format(css_string=css_string)
    print(html)


if __name__ == "__main__":
    sys.exit(main())
