#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from itertools import chain
from datetime import time
from collections import namedtuple


SensorSection = namedtuple(
    "SensorSection", [
        "entry", "exit"])  # where the magic happens


def getSensorPosition(section_id):
    return float(section_id[3:7]) / 10


def getDistanceOfSensorSection(section):
    p_a = getSensorPosition(section[0])
    p_b = getSensorPosition(section[1])
    return abs(p_b - p_a)

"""
    Split 24 hours to by given interval(minutes).
    e.g. [ "0:00", "0:05", ..., "23:55" ]
"""


def splitDay(interval):
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

    return [t.strftime("%H:%M") for t in result]


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
        with open(fname, 'r') as f:
            reader = csv.reader(f, dialect=dia, delimiter=deli)
            return [tuple(r) for r in reader]

    """
        @data: list or something...
        @other parameters same as above
    """
    @staticmethod
    def write(data, fname, dia='excel', deli=','):
        with open(fname, 'w') as f:
            writer = csv.writer(f, dialect=dia, delimiter=deli)
            for r in data:
                writer.writerow(r)

    @staticmethod
    def save(data, dest):
        if not 'output' in os.listdir('.'):
            os.mkdir('output')
        CSVUtil.write(data, dest)
#------------- END CSVUtil ------------------


# Helper Functions
def subdirs(path):
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            yield entry.name


def subfiles(path):
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            yield entry.name


def listdir(path):
    for entry in os.scandir(path):
        if not entry.name.startswith('.'):
            yield entry.name

"""
    From [(1,2), (3,4)]
    To   [1, 2, 3, 4]

    Note: Using this to avoid nested loops
"""


def flatList(lst):
    return list(chain.from_iterable(lst))  # itertools.chain


def mappedList(fn, iteralbe):
    return list(map(fn, iteralbe))


def sumMappedList(fn, iteralbe):
    return sum(list(map(fn, iteralbe)))


def printList(obj):
    for i, e in enumerate(obj):
        if i == 3:
            break
        else:
            print(e)
            i += 1


def printDict(obj):
    i = 0
    for k, v in obj.items():
        if i == 3:
            break
        else:
            print("{} -> {}".format(k, v))
            i += 1


if __name__ == "__main__":
    csvutil = CSVUtil()
    data = csvutil.read('./output/20150702.csv')
    for e in data:
        if len(e) > 291:
            print("Got you")
