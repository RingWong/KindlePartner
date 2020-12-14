# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

import os
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, \
    QRadioButton, QGroupBox, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from common import RunningCommand, whether_running_command_is_available, custom_logger


class RunningMessageThread(QThread):
    running_signal = pyqtSignal()

    def __init__(self, pipe):
        super(RunningMessageThread, self).__init__()
        self.pipe = pipe

    def run(self):
        while True:
            msg = self.pipe.recv()
            self.running_signal.emit()


class KindlePartnerMainWindow(QWidget):
    def __init__(self, command_queue, pipe, config):
        super(KindlePartnerMainWindow, self).__init__()
        self.command_queue = command_queue
        self.config = config
        self.input_file_path_button = QPushButton("选择文件")
        self.input_file_path_line_edit = QLineEdit()
        self.note_filter_keep_tag_radio_button = QRadioButton("仅保留标注文本")
        self.note_filter_keep_all_radio_button = QRadioButton("保留文本、位置与时间")
        self.sorted_key_combo_box = QComboBox()
        self.sorted_order_combo_box = QComboBox()
        self.output_file_path_button = QPushButton("选择文件夹")
        self.output_file_path_line_edit = QLineEdit()
        self.running_info_label = QLabel()
        self.run_button = QPushButton("运行")
        self.quit_button = QPushButton("退出")
        self.running_message_thread = RunningMessageThread(pipe)
        self.running_message_thread.running_signal.connect(self._run_button_enable)
        self.running_message_thread.start()

        self.initUI()

    def initUI(self):
        # input info
        input_info_layout = QHBoxLayout()
        input_group_box = QGroupBox("输入文件信息", self)
        input_file_path_label = QLabel("My Clippings.txt文件路径:")

        self.input_file_path_line_edit.setEnabled(False)
        self.input_file_path_button.clicked.connect(
            self._input_file_path_button_click)

        input_info_layout.addWidget(input_file_path_label)
        input_info_layout.addWidget(self.input_file_path_line_edit)
        input_info_layout.addWidget(self.input_file_path_button)

        input_group_box.setLayout(input_info_layout)

        # note filter info
        note_filter_info_layout = QHBoxLayout()
        note_filter_group_box = QGroupBox("笔记过滤", self)

        self.note_filter_keep_tag_radio_button.setChecked(True)

        note_filter_info_layout.addWidget(
            self.note_filter_keep_tag_radio_button)
        note_filter_info_layout.addWidget(
            self.note_filter_keep_all_radio_button)

        note_filter_group_box.setLayout(note_filter_info_layout)

        # sort info
        sorted_info_layout = QGridLayout()
        sorted_group_box = QGroupBox("排序策略", self)
        sorted_key_label = QLabel("排序依据:")
        sorted_order_label = QLabel("排序顺序:")

        self.sorted_key_combo_box.addItems(
            self.config.get('sorted_info', {}).get('sorted_key', {}).keys())
        self.sorted_order_combo_box.addItems(
            self.config.get('sorted_info', {}).get('sorted_order', {}).keys())

        sorted_info_layout.addWidget(sorted_key_label, 0, 0)
        sorted_info_layout.addWidget(self.sorted_key_combo_box, 0, 1)
        sorted_info_layout.addWidget(sorted_order_label, 1, 0)
        sorted_info_layout.addWidget(self.sorted_order_combo_box, 1, 1)

        sorted_group_box.setLayout(sorted_info_layout)

        # output info
        output_info_layout = QGridLayout()
        output_group_box = QGroupBox("输出文件信息", self)
        output_file_type_label = QLabel("输出文件类型:")
        output_file_combo_box = QComboBox()

        output_file_combo_box.addItems(
            self.config.get('output_info', {}).get('output_file_type', []))
        output_file_path_label = QLabel("输出文件存放路径:")

        self.output_file_path_button.clicked.connect(
            self._output_file_path_button_click)
        self.output_file_path_line_edit.setEnabled(False)

        output_info_layout.addWidget(output_file_type_label, 0, 0)
        output_info_layout.addWidget(output_file_combo_box, 0, 1)
        output_info_layout.addWidget(output_file_path_label, 1, 0)
        output_info_layout.addWidget(self.output_file_path_line_edit, 1, 1)
        output_info_layout.addWidget(self.output_file_path_button, 1, 2)

        output_group_box.setLayout(output_info_layout)

        # run or quit
        running_action_layout = QHBoxLayout()

        self.run_button.clicked.connect(self._run_button_click)
        self.quit_button.clicked.connect(self._quit_button_click)

        running_action_layout.addWidget(self.run_button)
        running_action_layout.addWidget(self.quit_button)

        # final
        main_layout = QVBoxLayout()

        main_layout.addWidget(input_group_box)
        main_layout.addWidget(note_filter_group_box)
        main_layout.addWidget(sorted_group_box)
        main_layout.addWidget(output_group_box)
        main_layout.addWidget(self.running_info_label)
        main_layout.addLayout(running_action_layout)

        self.setWindowTitle("Kindle Partner")
        self.setLayout(main_layout)

    @pyqtSlot()
    def _input_file_path_button_click(self):
        input_file_path, _ = QFileDialog.getOpenFileName(
            self, "选择My_Clippings.txt文件", os.getcwd(),
            "All Files (*);;Text Files (*.txt)")
        self.input_file_path_line_edit.setText(input_file_path)

    @pyqtSlot()
    def _output_file_path_button_click(self):
        output_file_path = QFileDialog.getExistingDirectory(
            self, "选择存放输出文件的文件夹", os.getcwd())
        self.output_file_path_line_edit.setText(output_file_path)

    @pyqtSlot()
    def _run_button_enable(self):
        self.run_button.setEnabled(True)
        self.running_info_label.setText("运行完毕")
        custom_logger.info("Done.")

    @pyqtSlot()
    def _run_button_click(self):
        sorted_key = self.sorted_key_combo_box.currentText()
        sorted_key = self.config.get('sorted_info',
                                     {}).get('sorted_key',
                                             {}).get(sorted_key, None)

        reverse_or_not = self.sorted_order_combo_box.currentText()
        reverse_or_not = self.config.get('sorted_info', {}).get(
            'sorted_order', {}).get(reverse_or_not, False)

        if self.note_filter_keep_all_radio_button.isChecked():
            keep_all = True
        else:
            keep_all = False

        running_command = RunningCommand(self.input_file_path_line_edit.text(),
                                         self.output_file_path_line_edit.text(),
                                         sorted_key, reverse_or_not, keep_all)
        custom_logger.info(running_command)

        if not whether_running_command_is_available(running_command):
            QMessageBox.warning(self, "警告", "输入文件不存在，请重新指定。", QMessageBox.Ok)
            custom_logger.info("Input file not exists.")
            return

        remain_info = "将对{}进行处理，结果存放在{}".format(
            self.input_file_path_line_edit.text(),
            self.output_file_path_line_edit.text())

        message_before_running = QMessageBox.question(
            self, "确认运行信息", remain_info, QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes)

        if message_before_running == QMessageBox.Yes:
            self.command_queue.put(running_command)

            self.run_button.setEnabled(False)
            self.running_message_thread.start()
            self.running_info_label.setText("运行中...")
            self.running_info_label.show()

    @pyqtSlot()
    def _quit_button_click(self):
        self.close()


if __name__ == "__main__":
    pass
