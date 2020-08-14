# -*- coding: utf-8 -*-

"""
    Created by RonWong

"""


def sort_by_location(clipping_items: list):
    sorted_clipping_items = list(sorted(clipping_items, key=lambda x: x.location, reverse=False))
    return sorted_clipping_items


def save_to_txt(file_path, clipping_items: list):
    with open(file_path, mode="w+", encoding="urt-8", errors="ignore") as wf:
        for clipping_item in clipping_items:
            pass