#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from itertools import chain

class CSVUtil:

    def __init__(self):
        pass

    """
        @fname: file name
        @deli: delimiter (default to excel)
        @dialect: excel or excel-tab (default to comma)
    """
    @staticmethod
    def read(fname, dia='excel', deli=','):
        with open(fname, 'r', encoding='utf8') as f:
            reader = csv.reader(f, dialect=dia, delimiter=deli)
            return [tuple(row) for row in reader]

    """
        @data: list or something...
        @other parameters same as above
    """
    @staticmethod
    def write(data, fname, dia='excel', deli=','):
        with open(fname, 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f, dialect=dia, delimiter=deli)
            for r in data:
                writer.writerow(r)

    @staticmethod
    def save(data, dest):
        if not 'output' in os.listdir('.'):
            os.mkdir('output')
        CSVUtil.write(data, dest)

def subdirs(path):
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            yield entry.name


def subfiles(path):
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            yield entry.name

def flatList(lst):
    return list(chain.from_iterable(lst))  # itertools.chain

if __name__ == "__main__":
    result = []
    read = CSVUtil.read
    write = CSVUtil.write

    def remain_needed(filename, idx):
        data = read(filename)
        if idx > 0:
            return data[1:]
        elif idx == 0:
            return data

    files = enumerate(subfiles("."))
    result = [ remain_needed(filename, idx) for idx, filename in files \
                                            if not filename.endswith(".py")]
    result = flatList(result)

    write(result, "./審核結果總檔.csv")


