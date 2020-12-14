# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

import os
import yaml
import logging
from threading import Lock, Thread
from collections import namedtuple


class RunningCommand(namedtuple("RunningCommand", [
    "inputfile", "outputfile", "sortedkey",
    "reverse", "keepall"])):

    def __str__(self):
        output_str = " ".join("{}={}".format(str(key), str(value)) for key, value in self._asdict().items())
        return "{}: {}".format(self.__class__.__name__, output_str)


ClippingItem = namedtuple("ClippingItem", [
    "bookname", "marktype", "location", "create_time", "content"])


def load_yaml_config(file_path):
    with open(file_path, encoding="utf-8") as rf:
        yaml_stream = rf.read()
    return yaml.load(yaml_stream, Loader=yaml.FullLoader)


def whether_running_command_is_available(running_command: RunningCommand) -> bool:
    input_file_exists = os.path.exists(running_command.inputfile)
    if not input_file_exists:
        print("Input file dosen't exists.")
        return False

    output_file_exists = os.path.isdir(running_command.outputfile)
    if not output_file_exists:
        print(
            "Output directory dosen't exists. It will be created automatically."
        )
        os.makedirs(running_command.outputfile)

    return True


class Logger(object):
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, log_path, clevel=logging.DEBUG, flevel=logging.DEBUG):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)

        fh = logging.FileHandler(log_path)
        fh.setFormatter(fmt)
        fh.setLevel(flevel)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


custom_logger = Logger(os.path.join(os.getcwd(), 'kindle_partner.log'))
