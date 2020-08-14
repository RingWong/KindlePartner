# -*- coding: utf-8 -*-

"""
    Created by RonWong

"""

import regex as re
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict


ClippingItem = namedtuple("ClippingItem", ["bookname", "marktype", "location", "datetime", "content"])


class ClippingFile(object):
    def __init__(self, split_mark="==========", item_size=5):
        self.split_mark = split_mark
        self.item_size = item_size
        self.clipping_item = ClippingItem
        self.clipping_record = defaultdict(list)
        self.original_lines = list()
        self.date_pattern = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")
        self.time_pattern = re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}")
        self.afternoon_pattern = re.compile(r"下午")
        self.location_pattern = re.compile(r"#[0-9|-]+")
        self.marktype_pattern = re.compile(r"(([书][签])|([标][注]))")

    def _load_file(self, file_path):
        with open(file_path, encoding="utf-8", errors="ignore") as rf:
            lines = rf.readlines()

        lines_effective_len = len(lines) // self.item_size * self.item_size
        left_idxs = [i for i in range(0, lines_effective_len, self.item_size)]
        right_idxs = [i + self.item_size for i in range(0, lines_effective_len, self.item_size)]

        for left_idx, right_idx in zip(left_idxs, right_idxs):
            self.original_lines.append(lines[left_idx: right_idx])

    def _get_datetime(self, line: str) -> "datetime":
        date_match_group = re.search(self.date_pattern, line)
        time_match_group = re.search(self.time_pattern, line)
        afternoon_match_group = re.search(self.afternoon_pattern, line)

        if date_match_group and time_match_group:
            date_str = date_match_group.group(0).replace("年", "-").replace("月", "-").replace("日", " ")
            time_str = time_match_group.group(0)
            datetime_str = date_str + time_str
            clipping_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

            if afternoon_match_group:
                clipping_datetime += timedelta(hours=12)

        else:
            clipping_datetime = datetime.now()

        return clipping_datetime

    def _get_location_and_marktype(self, line: str):
        location_match_group = re.search(self.location_pattern, line)
        marktype_match_group = re.search(self.marktype_pattern, line)

        location = location_match_group.group(0) if location_match_group else None
        marktype = marktype_match_group.group(0) if marktype_match_group else None

        return location, marktype

    def run(self, file_path):
        self._load_file(file_path)

        for original_item in self.original_lines:
            
            bookname = original_item[0].strip()
            location_line, datetime_line = original_item[1].split("|")
            location, marktype = self._get_location_and_marktype(location_line)
            clipping_datetime = self._get_datetime(datetime_line)
            content = original_item[3].strip()

            clipping_item = self.clipping_item(bookname, marktype, location, clipping_datetime, content)

            self.clipping_record[bookname].append(clipping_item)

    @property
    def book2clippingitems(self):
        return self.clipping_record


if __name__ == "__main__":
    s = "添加于 2018年11月17日星期六 下午11:19:49 "
    # pattern = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")
    # pattern = re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}")
    # print(re.search(pattern, s).group(0))

    clipping_file = ClippingFile()
    print(clipping_file._get_datetime(s))
    # print(datetime.now())
    # result = filter(str.isdigit, s)
    # result = ''.join(result)

    # datetime.strptime()


