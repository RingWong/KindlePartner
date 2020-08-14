# -*- coding: utf-8 -*-

"""
    Created by RonWong

"""

import sys
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QComboBox


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        self.setLayout(grid_layout)

        # self._add_widget("button", "OK", grid_layout, 1, 1)
        # self._add_widget("button", "Exit", grid_layout, 1, 2)

        # self._add_widget("label", "My Clippings.txt文件路径:", 1, 0)

        input_file_path_label = QLabel("My Clippings.txt文件路径:")
        input_file_path_line_edit = QLineEdit()
        
        output_file_type_label = QLabel("输出文件类型:")
        output_file_combo_box = QComboBox()
        output_file_combo_box.addItem("txt")

        output_file_path_label = QLabel("输出文件存放路径:")
        output_file_path_line_edit = QLineEdit()


        self.setWindowTitle("Demo")
        self.show()

    # def _add_widget(self, widget_type, widget_text, layout, *args):
    #     if widget_type == "button":
    #         widget_function = QPushButton
    #     elif widget_type == "label":
    #         widget_function = QLabel
    #     else:
    #         return

    #     widget = widget_function(widget_text)
    #     layout.addWidget(widget, *args)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())




