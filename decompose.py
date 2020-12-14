# -*- coding: utf-8 -*-
"""
    Created by RonWong

"""

import os
import regex as re
from datetime import datetime, timedelta
from collections import defaultdict
from common import ClippingItem, RunningCommand, whether_running_command_is_available
from multiprocessing.queues import JoinableQueue


class ClippingFile(object):
    def __init__(self):
        self.split_mark = "=========="
        self.item_size = 5
        self.clipping_item_type = ClippingItem
        self.clipping_record = defaultdict(list)
        self.original_lines = list()
        self.bookname_pattern = re.compile(r"[^\u4e00-\u9fa5a-zA-Z]")
        self.date_pattern = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")
        self.time_pattern = re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}")
        self.pm_pattern = re.compile(r"下午")
        self.location_pattern = re.compile(r"#[0-9|-]+")
        self.marktype_pattern = re.compile(r"(([书][签])|([标][注]))")

    def _load_file(self, load_file_path):
        with open(load_file_path, encoding="utf-8", errors="ignore") as rf:
            lines = rf.readlines()

        lines_effective_len = len(lines) // self.item_size * self.item_size
        left_idxs = [i for i in range(0, lines_effective_len, self.item_size)]
        right_idxs = [
            i + self.item_size
            for i in range(0, lines_effective_len, self.item_size)
        ]

        for left_idx, right_idx in zip(left_idxs, right_idxs):
            self.original_lines.append(lines[left_idx:right_idx])

    def _save_file(self, output_file_path, clipping_items: list,
                   keep_all: bool = False):
        if keep_all:
            save_data = ("{} {} \n {} \n {} \n".format(
                         clipping_item.location, clipping_item.create_time,
                         clipping_item.content, self.split_mark)
                         for clipping_item in clipping_items)
        else:
            save_data = ("{}\n".format(clipping_item.content)
                         for clipping_item in clipping_items)

        with open(output_file_path,
                  mode="w",
                  encoding="utf-8",
                  errors="ignore") as wf:
            for data in save_data:
                wf.write(data)

    def _get_datetime(self, line: str) -> "datetime":
        date_match_group = re.search(self.date_pattern, line)
        time_match_group = re.search(self.time_pattern, line)
        afternoon_match_group = re.search(self.pm_pattern, line)

        if date_match_group and time_match_group:
            date_str = date_match_group.group(0).replace("年", "-").replace(
                "月", "-").replace("日", " ")
            time_str = time_match_group.group(0)
            datetime_str = date_str + time_str
            clipping_datetime = datetime.strptime(datetime_str,
                                                  "%Y-%m-%d %H:%M:%S")

            if afternoon_match_group:
                clipping_datetime += timedelta(hours=12)

        else:
            clipping_datetime = datetime.now()

        return clipping_datetime

    def _get_location_and_marktype(self, line: str):
        location_match_group = re.search(self.location_pattern, line)
        marktype_match_group = re.search(self.marktype_pattern, line)

        location = location_match_group.group(
            0) if location_match_group else None
        marktype = marktype_match_group.group(
            0) if marktype_match_group else None

        return location, marktype

    @staticmethod
    def _sort_clipping_items(clipping_items: list,
                             key='location',
                             reverse=False):

        sorted_clipping_items = sorted(
            clipping_items,
            key=lambda clipping_item: getattr(clipping_item, key),
            reverse=reverse)

        return sorted_clipping_items

    def _split_file(self, running_command: "RunningCommand"):
        if not whether_running_command_is_available(running_command):
            exit(1)

        self._load_file(running_command.inputfile)

        for original_item in self.original_lines:
            content = original_item[3].strip()

            # skip bookmark clipping record
            if len(content) == 0:
                continue

            location_line, datetime_line = original_item[1].split("|")
            location, marktype = self._get_location_and_marktype(location_line)

            bookname = re.sub(self.bookname_pattern, "", original_item[0])

            create_time = self._get_datetime(datetime_line)

            clipping_item = self.clipping_item_type(bookname, marktype,
                                                    location, create_time,
                                                    content)

            self.clipping_record[bookname].append(clipping_item)

        for bookname, clipping_items in self.clipping_record.items():
            self.clipping_record[bookname] = self._sort_clipping_items(
                clipping_items,
                key=running_command.sortedkey,
                reverse=running_command.reverse)
            self._save_file(
                os.path.join(running_command.outputfile,
                             "{}.txt".format(bookname)),
                self.clipping_record[bookname],
                keep_all=running_command.keepall)

    def run(self, data, pipe=None):
        if type(data) == JoinableQueue:
            while True:
                running_command = data.get()
                self._split_file(running_command)
                print(running_command)
                data.task_done()

                if pipe:
                    pipe.send("Running Command Done.")

        elif type(data) == RunningCommand:
            self._split_file(data)


if __name__ == "__main__":
    pass
