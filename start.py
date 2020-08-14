# -*- coding: utf-8 -*-

"""
    Created by RonWong

"""

from decompose import ClippingFile
from utils import sort_by_location


if __name__ == "__main__":
    clipping_file = ClippingFile()
    clipping_file.run('sample.txt')
    print(clipping_file.book2clippingitems)
