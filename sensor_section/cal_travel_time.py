g#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import math
from utils import CSVUtil

"""
    Input Data: TDCS_M04A_[date]_[time]
    Data Format:
        row[0], row[1], row[2], row[3], row[4], row[5]
        date_time,  etc_entrance, etc_exit, car_type, mean_travel_time, num_cars
"""

DATA_EXT = '.csv'
NUM_CAR_TYPE = 5

def save(result, fname):
    dirname = 'output'
    file_ext = '.csv'
    if dirname not in os.listdir('.'):
        os.mkdir(dirname)
    fname = os.path.splitext(fname)[0]  # remove file extension
    fname = fname.split('_', 2)[-1]  # retain date from orignal file name
    fname += '_s1tt' + file_ext
    csv.write(result, dirname + '/' + fname)

"""
    @ Calcuate mean travel time of all types of cars between two ETC stations by:
        * mean travel time (mtt_c)
        * number of cars (nc_c)
        * c means car's type

    @ Formula (for each ETC segment):
        floor(
            (mtt_1 * nc_1) + (mtt_2 * nc_2) + ... + (mtt_5 * nc_5) /
            (nc_1 + nc_2 + ... + nc_5)
        )

    @ Note:
        * if no car pass the ETC section, then the travel time will be:
          ETC_section_distance(km) / 80(km/h) * 3600

"""
def calc_s1tt(fname):
    data = csv.read(fname)
    c = 0
    numerator = 0
    denominator = 0
    result = []
    for row in data:
        c += 1
        numerator += int(row[4]) * int(row[5])
        denominator += int(row[5])
        if c > 0 and c % NUM_CAR_TYPE == 0 and denominator > 0:
            s1tt = math.floor(numerator / denominator)
            result.append((row[1], row[2], s1tt))
            numerator = 0
            denominator = 0
    save(result, fname)

def run(arg):
    csv = CSVUtil()
    if arg.endswith(DATA_EXT):  # file
        fname = arg
        calc_s1tt(fname)
    else:  # dir
        os.chdir(arg)
        files = os.listdir('.')
        for fname in files:
            if fname.endswith(DATA_EXT):
                calc_s1tt(fname)



if __name__ == "__main__":
    csv = CSVUtil()
    args = sys.argv[1:]

    if not args:
        print('Give me a file name or directory')
        sys.exit(1)
    else:
        for arg in args:
            run(arg)
