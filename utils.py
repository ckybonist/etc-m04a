#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from datetime import time

## Helper Functions
def listdirNoHidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

"""
    Generate a list like: [ "0:00", "0:05", ..., "23:55" ]
"""
def createSensingIntervals(interval):
    NUM_HOURS = 24
    NUM_INTERVALS_EACH_HOUR = int(60 / interval)

    hour = 0
    minute = 0
    result = [time(hour, minute)]

    for i in range(NUM_HOURS):
        for j in range(NUM_INTERVALS_EACH_HOUR):
            minute += interval
            if minute == 60:
                hour += 1
                minute = 0
            if hour == 24:
                break
            result.append(time(hour, minute))


    to_str = lambda t: t.strftime("%H:%M")
    result = list(map(to_str, result))
    return result


class CSVUtil:
    def __init__(self):
        pass
    """
        @fname: file name
        @deli: delimiter (default to excel)
        @dialect: excel or excel-tab (default to comma)
    """
    @staticmethod
    def read(fname, dia = 'excel', deli = ','):
        with open(fname, 'r') as f:
            reader = csv.reader(f, dialect = dia, delimiter = deli)
            return [ tuple(r) for r in reader ]

    """
        @data: list or something...
        @other parameters same as above
    """
    @staticmethod
    def write(data, fname, dia = 'excel' , deli = ','):
        with open(fname, 'w') as f:
            writer = csv.writer(f, dialect = dia, delimiter = deli)
            for r in data:
                writer.writerow(r)

    @staticmethod
    def save(data, dest):
        if not 'output' in os.listdir('.'):
            os.mkdir('output')
        CSVUtil.write(data, dest)


if __name__ == "__main__":
    csvutil = CSVUtil()
    data = csvutil.read('./output/20150702.csv')
    for e in data:
        if len(e) > 291:
            print("Got you")
