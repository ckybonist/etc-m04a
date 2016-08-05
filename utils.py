#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from itertools import chain
from datetime import time
from collections import namedtuple
from config import TIME_INTERVAL


SensorSection = namedtuple("SensorSection", ["entry", "exit"])  # where the magic happens
InterchangeSection = namedtuple("InterchangeSection", ["start", "dest"])  # where the magic happens

def saveResult(step, anchor, filename, content):
    from config import OUTPUT_DIR

    if "output" not in subdirs('.'):
        os.mkdir("output")

    path = "{}/{}/{}".format(OUTPUT_DIR, step, anchor)
    if path not in subdirs(OUTPUT_DIR):
        os.makedirs(path, exist_ok=True)
    dest = "{}/{}".format(path, filename)

    CSVUtil.save(content, dest)

def getSensorLocation(section_id):
    return float(section_id[3:7]) / 10


def getDistanceOfSensorSection(section):
    loc_a = getSensorLocation(section[0])
    loc_b = getSensorLocation(section[1])
    result = abs(loc_b - loc_a)
    return (result, loc_a, loc_b)

"""
    Split 24 hours to by given interval(minutes).
    e.g. [ "0:00", "0:05", ..., "23:55" ]
"""


def splitDay():
    NUM_HOURS = 24
    NUM_INTERVALS_EACH_HOUR = int(60 / TIME_INTERVAL)

    hour = 0
    minute = 0
    result = [time(hour, minute)]

    for i in range(NUM_HOURS):
        for j in range(NUM_INTERVALS_EACH_HOUR):
            minute += TIME_INTERVAL
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

def floatList(lst):
    return [ float(e) for e in lst ]


def flatList(lst):
    return list(chain.from_iterable(lst))  # itertools.chain


def mappedList(fn, *iteralbe):
    return list(map(fn, *iteralbe))


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
