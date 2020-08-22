# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

import yaml
from collections import namedtuple


ClippingItem = namedtuple("ClippingItem", [
    "bookname", "marktype", "location", "create_time", "content"])

RunningCommand = namedtuple("RunningCommand", [
    "input_file_path", "output_file_path", "sorted_key",
    "reverse", "keep_all"])


def load_yaml_config(file_path):
    with open(file_path, encoding="utf-8") as rf:
        yaml_stream = rf.read()
    return yaml.load(yaml_stream, Loader=yaml.FullLoader)
