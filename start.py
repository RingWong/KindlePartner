# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

from multiprocessing import Process, JoinableQueue, Pipe
import sys
import argparse
from decompose import ClippingFile
from PyQt5.QtWidgets import QApplication
from qt_ui import KindlePartnerMainWindow
from common import RunningCommand, load_yaml_config


def frontend_function(*args):
    app = QApplication(sys.argv)
    main_window = KindlePartnerMainWindow(*args)
    main_window.show()
    sys.exit(app.exec_())


def backend_function(*args):
    clipping_file = ClippingFile()
    clipping_file.run(*args)


def activite_ui():
    print("Activate UI")

    config = load_yaml_config("ui.yaml")

    running_command_queue = JoinableQueue()
    pipe = Pipe()

    frontend_process = Process(target=frontend_function,
                               args=(running_command_queue, pipe[0], config))
    frontend_process.start()

    backend_process = Process(target=backend_function,
                              args=(running_command_queue, pipe[1]),
                              daemon=True)
    backend_process.start()

    frontend_process.join()

    running_command_queue.join()


def activite_cmd():
    print("Activate CMD")

    args = parse_cmd_args()
    running_command = RunningCommand(args.inputfile, args.outputfile,
                                     args.sortedtype, args.reverse,
                                     args.keepbookmark)

    backend_function(running_command)


def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Kindle Partner.")
    parser.add_argument("inputfile", help="The path to My Clippings.txt")
    parser.add_argument("outputfile", help="The path to store output file.")
    parser.add_argument(
        "-k",
        dest="sortedkey",
        choices=["location", "create_time"],
        type=str,
        default="location",
        help="use which key to sort the result, default is the location in clipping record."
    )
    parser.add_argument("-r",
                        dest="reverse",
                        action="store_true",
                        help="whether to reverse the sorted result.")
    parser.add_argument("-a",
                        dest="keepall",
                        action="store_true",
                        help="whether to keep all detail in output file.")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    if len(sys.argv) == 1:
        activite_ui()
    elif len(sys.argv) >= 3:
        activite_cmd()
