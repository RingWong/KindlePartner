# -*- coding: utf-8 -*-

"""
    Created by RonWong

"""

import sys
import os
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QComboBox, \
    QRadioButton, QGroupBox, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.input_file_path_button = QPushButton("选择文件")
        self.input_file_path_line_edit = QLineEdit()
        self.sorted_type_location_radio_button = QRadioButton("标注位置")
        self.sorted_type_clipping_datetime_radio_button = QRadioButton("标注时间")
        self.sorted_type_clipping_datetime_combo_box = QComboBox()
        self.output_file_path_button = QPushButton("选择文件夹")
        self.output_file_path_line_edit = QLineEdit()
        self.run_button = QPushButton("运行")
        self.quit_button = QPushButton("退出")
        # self.message_box_before_running = 

        self.initUI()

    def initUI(self):
        # input info
        input_info_layout = QHBoxLayout()
        input_group_box = QGroupBox("输入文件信息", self)
        input_file_path_label = QLabel("My Clippings.txt文件路径:")
        
        self.input_file_path_line_edit.setEnabled(False)
        self.input_file_path_button.clicked.connect(self._input_file_path_button_click)

        input_info_layout.addWidget(input_file_path_label)
        input_info_layout.addWidget(self.input_file_path_line_edit)
        input_info_layout.addWidget(self.input_file_path_button)

        input_group_box.setLayout(input_info_layout)

        # sort info
        sorted_info_layout = QHBoxLayout()
        sorted_group_box = QGroupBox("文件排序方式", self)

        self.sorted_type_location_radio_button.setChecked(True)
        self.sorted_type_location_radio_button.clicked.connect(
            self._sorted_type_location_radio_button_click)
        self.sorted_type_clipping_datetime_radio_button.clicked.connect(
            self._sorted_type_clipping_datetime_radio_button_click)
        self.sorted_type_clipping_datetime_combo_box.addItems(["按时间升序", "按时间降序"])
        self.sorted_type_clipping_datetime_combo_box.setEnabled(False)

        sorted_info_layout.addWidget(self.sorted_type_location_radio_button)
        sorted_info_layout.addWidget(self.sorted_type_clipping_datetime_radio_button)
        sorted_info_layout.addWidget(self.sorted_type_clipping_datetime_combo_box)

        sorted_group_box.setLayout(sorted_info_layout)

        # output info
        output_info_layout = QGridLayout()
        output_group_box = QGroupBox("输出文件信息", self)
        output_file_type_label = QLabel("输出文件类型:")
        output_file_combo_box = QComboBox()
        output_file_combo_box.addItem("txt")
        output_file_path_label = QLabel("输出文件存放路径:")
        self.output_file_path_button.clicked.connect(self._output_file_path_button_click)
        self.output_file_path_line_edit.setEnabled(False)

        output_info_layout.addWidget(output_file_type_label, 0, 0)
        output_info_layout.addWidget(output_file_combo_box, 0, 1)
        output_info_layout.addWidget(output_file_path_label, 1, 0)
        output_info_layout.addWidget(self.output_file_path_line_edit, 1, 1)
        output_info_layout.addWidget(self.output_file_path_button, 1, 2)

        output_group_box.setLayout(output_info_layout)

        # run or quit
        running_info_layout = QHBoxLayout()

        self.run_button.clicked.connect(self._run_button_click)
        self.quit_button.clicked.connect(self._quit_button_click)

        running_info_layout.addWidget(self.run_button)
        running_info_layout.addWidget(self.quit_button)

        # final
        main_layout = QVBoxLayout()
        main_layout.addWidget(input_group_box)
        main_layout.addWidget(sorted_group_box)
        main_layout.addWidget(output_group_box)
        main_layout.addLayout(running_info_layout)
 
        self.setWindowTitle("Kindle Partner")

        self.setLayout(main_layout)

        self.show()
    
    @pyqtSlot()
    def _sorted_type_location_radio_button_click(self):
        self.sorted_type_clipping_datetime_combo_box.setEnabled(False)
    
    @pyqtSlot()
    def _sorted_type_clipping_datetime_radio_button_click(self):
        self.sorted_type_clipping_datetime_combo_box.setEnabled(True)
    
    @pyqtSlot()
    def _input_file_path_button_click(self):
        input_file_path, _ = QFileDialog.getOpenFileName(self, "选择My_Clippings.txt文件", os.getcwd(), "All Files (*);;Text Files (*.txt)")
        self.input_file_path_line_edit.setText(input_file_path)

    @pyqtSlot()
    def _output_file_path_button_click(self):
        output_file_path = QFileDialog.getExistingDirectory(self, "选择存放输出文件的文件夹", os.getcwd())
        self.output_file_path_line_edit.setText(output_file_path)
    
    @pyqtSlot()
    def _run_button_click(self):
        remain_info = "将对{}进行处理，结果存放在{}。确认？".format(self.input_file_path_line_edit.text(), self.output_file_path_line_edit.text())
        message = QMessageBox.question(self, '确认运行信息', remain_info, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if message == QMessageBox.Yes:
            pass

    @pyqtSlot()
    def _quit_button_click(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())




