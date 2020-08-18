# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

from collections import namedtuple


ClippingItem = namedtuple("ClippingItem", [
    "bookname", "marktype", "location", "create_time", "content"])

RunningCommand = namedtuple("RunningCommand", [
    "input_file_path", "output_file_path", "multi_process", "sorted_key",
    "reverse", "keep_bookmark"
])

