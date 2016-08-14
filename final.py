#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from statistics import median

from config import *
from utils import *

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def calc(datas, attr_info, headers, date):
    tmp_a = list(zip(*datas))
    tmp_b = [ list(zip(*row)) for row in tmp_a ]

    tmp_b = [ list(map(int, e)) for p in tmp_b for e in p]
    result = [ round(median(e)) for e in tmp_b ]
    result = chunks(result, 288)

    result = [ h + e for h, e in zip(headers, result) ]
    result = [list(attr_info)] + result

    CSVUtil.write(result, "../../../output/final/" + date + ".csv")

def getPathId(path):
    return MYPATHS.index(tuple(path)) + 1

def finalMedianTime():
    attr_info = []
    header = []

    for dir in subdirs("output/step3/"):
        date = dir
        datas = []
        os.chdir("output/step3/" + dir)
        for file in subfiles("."):
            data = CSVUtil.read(file)
            attr_info = ["日期", "路徑編號"] + list(data[0][4:])
            data = data[1:]
            headers = [[date, getPathId(e[1:4])] for e in data]
            data = [ e[4:] for e in data ]
            datas.append(data)
        calc(datas, attr_info, headers, date)
        os.chdir("../../../")


def sortByTime(lst):
    result = sorted(lst, key = lambda x: datetime.datetime.strptime(x[0], "%Y%m%d"))
    return result


def concatResult():
    result = []
    csv_read = CSVUtil.read
    csv_write = CSVUtil.write
    prefix = "output/final/"
    output_name = "ETC_FGU_FINAL.csv"

    def remain_needed(filename, idx):
        data = csv_read(filename)
        if idx > 0:
            return data[1:]
        elif idx == 0:
            return data

    files = enumerate(subfiles(prefix))
    result = [ remain_needed(prefix+filename, idx) for idx, filename in files \
                                            if not filename.endswith(".py") and
                                               not filename == output_name]
    result = flatList(result)
    attr_info = list(result[0])
    result = [attr_info] + sortByTime(result[1:])
    csv_write(result, "output/" + output_name)

def run():
    if "final" not in subdirs("output"):
        os.mkdir("output/final")

    finalMedianTime()
    concatResult()

if __name__ == "__main__":
    run()
