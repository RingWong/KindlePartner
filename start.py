# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

from multiprocessing import Process, JoinableQueue, cpu_count
import sys
import argparse
from decompose import ClippingFile
from PyQt5.QtWidgets import QApplication
from qt_ui import KindlePartnerMainWindow
from utils import RunningCommand


def frontend_function(command_queue):
    app = QApplication(sys.argv)
    main_window = KindlePartnerMainWindow(command_queue)
    main_window.show()
    sys.exit(app.exec_())


def backend_function(running_command: "RunningCommand"):
    clipping_file = ClippingFile()
    clipping_file.run(running_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kindle Partner.")
    parser.add_argument("inputfile", help="The path to My Clippings.txt")
    parser.add_argument("outputfile", help="The path to store output file.")
    parser.add_argument("-k", dest="sortkey", choices=["location", "create_time"], type=str, default="location", help="use which key to sort the result, default is the location in clipping record.")
    parser.add_argument("-m", dest="multiprocess", action="store_true", help="whether to run the code with multi process.")
    parser.add_argument("-r", dest="reverse", action="store_true", help="whether to reverse the sorted result.")
    parser.add_argument("-b", dest="keepbookmark", action="store_true", help="whether to keep bookmark in output file.")
    args = parser.parse_args()

    backend_function(RunningCommand(args.inputfile, args.outputfile, args.multiprocess, args.sortkey, args.reverse, args.keepbookmark))

    # running_command_queue = JoinableQueue(cpu_count())

    # frontend_process = Process(target=frontend_function,
    #                            args=(running_command_queue, ))
    # frontend_process.start()

    # backend_process = Process(target=backend_function,
    #                           args=(running_command_queue, ))
    # backend_process.start()

    # frontend_process.join()
    # app = QApplication(sys.argv)
    # main_window = KindlePartnerMainWindow(running_command_queue)
    # main_window.show()
    # sys.exit(app.exec_())

    # backend_process.join()
    # running_command_queue.join()

    # sys.exit(app.exec_())




