#!/usr/bin/env python
# coding:utf-8

# GIMP Plug-in for the ZX-Spectrum binary screen file format

# Copyright (C) 2017 by João S. O. Bueno <gwidion@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Plug-in structure based on the Open Raster plug-in by Jn Nordy, on GIMP source tree.
from __future__ import print_function


from  gimpfu import *
import os, sys

SIZE = WIDTH, HEIGHT = 256, 192

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def save_speccy(img, drawable, filename, raw_filename):
    print("Not implemented")
    pass


def thumbnail_speccy(filename, thumbsize):
    return load_speccy(filename, filename)


def load_speccy(filename, raw_filename):
    path = raw_filename[len('file://'):]
    data = open(path, "rb").read()
    if len(data) != 6912:
        print("Incorrect file size for {}: probably not a zx-spectrum scr.".format(filename),
              file=sys.stderr)

    img = gimp.Image(WIDTH, HEIGHT, RGB)
    layer = img.new_layer(mode=RGB)
    def setter(coords, color):
        v = coords + (4, color + (255,) )
        pdb.gimp_drawable_set_pixel(layer, *v)
    load_bitmap(setter, data)
    return img


def pygame_load(scr, data):
    """Loads the bitmap data of a speccy image given a pygame surface and file data."""
    return load_bitmap(scr.set_at, data)


def load_bitmap(pixel_setter, data):
    """Loads a speccy image as a bitmap given a 'set_pixel' function and file data"""
    offset = 0
    block = 0
    col = 0
    line = 0
    data = bytearray(data)
    while True:
        row_data = data[offset: offset + 32]
        tmp = (offset // 32)
        line = 8 * (tmp % 8) + (tmp // 8) % 8 + 64 * ((offset // 2048))
        if line >= 192: break
        for col, byte in enumerate(row_data):
            for pix in range(7, -1, -1):
                pixel_setter((col * 8 + pix  , line), WHITE if byte & 0x01 else BLACK)
                byte >>= 1
        offset += 32


def register_load_handlers():
    gimp.register_load_handler('file-zxspectrum-load', 'scr', '')
    pdb['gimp-register-file-handler-mime']('file-zxspectrum-load', 'image/openraster')
    pdb['gimp-register-thumbnail-loader']('file-zxspectrum-load', 'file-zxspectrum-load-thumb')


def register_save_handlers():
    gimp.register_save_handler('file-zxspectrum-save', 'scr', '')


register(
    'file-zxspectrum-load-thumb', #name
    'loads a thumbnail from a ZX-Spectrum memory dump (.scr) file', #description
    'loads a thumbnail from a ZX-Spectrum memory dump (.scr) file',
    'João S. O. Bueno', #author
    'João S. O. Bueno', #copyright
    '2017', #year
    None,
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_INT, 'thumb-size', 'Preferred thumbnail size', None),
    ],
    [   #results. Format (type, name, description)
        (PF_IMAGE, 'image', 'Thumbnail image'),
        (PF_INT, 'image-width', 'Width of full-sized image'),
        (PF_INT, 'image-height', 'Height of full-sized image')
    ],
    thumbnail_speccy, #callback
)

register(
    'file-zxspectrum-save', #name
    'save a ZX-Spectrum image (.scr) file', #description
    'save a ZX-Spectrum image (.scr) file',
    'João S. O. Bueno', #author
    'João S. O. Bueno', #copyright
    '2017', #year
    'ZX-Spectrum',
    '*',
    [   #input args. Format (type, name, description, default [, extra])
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_STRING, "filename", "The name of the file", None),
        (PF_STRING, "raw-filename", "The name of the file", None),
    ],
    [], #results. Format (type, name, description)
    save_speccy, #callback
    on_query = register_save_handlers,
    menu = '<Save>'
)

register(
    'file-zxspectrum-load', #name
    'load a ZX-Spectrum image (.scr) file', #description
    """load a ZX-Spectrum image (.scr) file, generated from a video-map dump:
    a 6912 byte file 256x192 monochrome pixels + 768 bytes of color information.""",
    'João S. O. Bueno', #author
    'João S. O. Bueno', #copyright
    '2017', #year
    'ZX-Spectrum',
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_STRING, 'raw-filename', 'The name entered', None),
    ],
    [(PF_IMAGE, 'image', 'Output image')], #results. Format (type, name, description)
    load_speccy, #callback
    on_query = register_load_handlers,
    menu = "<Load>",
)


main()
