#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Input Data: TDCS_M04A_[date]_[time]
    Data Format:
        row[0], row[1], row[2], row[3], row[4], row[5]
        date_time,  etc_entrance, etc_exit, car_type, mean_travel_time, num_cars
"""

import os
import sys
import math
from collections import namedtuple, defaultdict

from utils import CSVUtil


## Constant
DATA_EXT = '.csv'
NUM_CAR_TYPE = 5
INPUT = '../data/'
OUTPUT = '../output/sensor_section/'
SensorSection = namedtuple("SensorSection", ["entry", "exit"])  # where the magic happens


## Helper Functions
def listdirNoHidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

### ====================== MAIN ============================
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
           1. -1
           2. ETC_section_distance(km) / 80(km/h) * 3600
           p.s.: #2 will apply when etc locations is settle down
"""
def calcTravelTimeStartAt(fname):
    csv = CSVUtil()
    data = csv.read(fname)
    avg_travel_time = lambda nu, de: math.floor(nu / de)
    result = []

    c = 0
    numerator = 0
    denominator = 0

    for row in data:
        c += 1
        numerator += int(row[4]) * int(row[5])
        denominator += int(row[5])

        if c > 0 and c % NUM_CAR_TYPE == 0:
            travel_time = -1 if denominator == 0 \
                             else avg_travel_time(numerator, denominator)

            sensor_section = SensorSection(entry=row[1], exit=row[2])
            result.append((sensor_section, travel_time))
            numerator = 0
            denominator = 0

    return result

def calcHourlyTravelTime(hour_dir):
    files = listdirNoHidden(hour_dir)
    prefix = './' + hour_dir + '/'
    result = []
    for f in files:
        f = prefix + f
        result.append(calcTravelTimeStartAt(f))
    return result


"""
    return result which has format like:
        { ETC_entry, ETC_exit, 0:00, 0:05, ..., 23:55 }
        NOTE: "0:00" means average travel time at 0:00

"""
def calcDailyTravelTime(path):
    os.chdir(path)
    hour_dirs = listdirNoHidden('.')
    tmpres = list(map(calcHourlyTravelTime, hour_dirs))
    print(tmpres[0][0][:10])

    result = defaultdict(list)  # where the magic happens
    # for hd in hour_dirs:
    #     files = listdirNoHidden(hd)
    #     prefix = './' + hd + '/'
    #     for f in files:
    #         f = prefix + f
    #         travel_time = calcTravelTimeStartAt(f)
    #         for k, v in travel_time:
    #             print("section: {}".format(k))
    #             print("Avg Time: {}".format(v))
    #             break
    #         break
    #     break
    #return result

def save(result, fname):
    dirname = 'output'
    file_ext = '.csv'
    if dirname not in os.listdir('.'):
        os.mkdir(dirname)
    fname = os.path.splitext(fname)[0]  # remove file extension
    fname = fname.split('_', 2)[-1]  # retain date from orignal file name
    fname += '_s1tt' + file_ext
    csv.write(result, dirname + '/' + fname)


def run(arg):
    if arg == "batch":
        pass
    elif arg == "test":  # for testing
        date = "20150702"
        path = INPUT + "201507/" + date
        result = calcDailyTravelTime(path)

### ============= End Main =======================



if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print('Give me a file name or directory')
        sys.exit(1)
    else:
        for arg in args:
            run(arg)
