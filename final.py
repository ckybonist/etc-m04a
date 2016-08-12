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

    result = [ list(h) + e for h in headers for e in result ]
    result = [list(attr_info)] + result

    CSVUtil.write(result, "../../../output/final/" + date + ".csv")

def test():
    mydir = "output/step3/20160820/"
    os.chdir(mydir)
    datas = []
    attr_info = []
    for file in subfiles("."):
        data = CSVUtil.read(file)
        attr_info = data[0]
        data = data[1:]
        headers = [e[:4] for e in data]
        data = [ e[4:] for e in data ]
        datas.append(data)
    calc(datas, attr_info, headers)

def finalMedianTime():
    attr_info = []
    header = []

    for dir in subdirs("output/step3/"):
        date = dir
        datas = []
        os.chdir("output/step3/" + dir)
        for file in subfiles("."):
            data = CSVUtil.read(file)
            attr_info = data[0]
            data = data[1:]
            headers = [e[:4] for e in data]
            data = [ e[4:] for e in data ]
            datas.append(data)
        calc(datas, attr_info, headers, date)
        os.chdir("../../../")

def run():
    if "final" not in subdirs("output"):
        os.mkdir("output/final")

    finalMedianTime()

if __name__ == "__main__":
    run()
