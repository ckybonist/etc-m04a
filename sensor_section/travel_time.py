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

from utils import CSVUtil, createSensingIntervals, listdirNoHidden


## Constant
DATA_EXT = '.csv'
NUM_CAR_TYPE = 5
TIME_INTERVAL = 5  # minutes
INPUT_DIR = '../data/'
OUTPUT_DIR = 'output/'
SensorSection = namedtuple("SensorSection", ["entry", "exit"])  # where the magic happens


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
    calcAvgTravelTime = lambda nu, de: math.floor(nu / de)
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
                             else calcAvgTravelTime(numerator, denominator)

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
    Merge hourly result to daily result (single dictionary)
    {
        SensorSection(entry, exit) : AvergeTravelTime
        ...
    }
"""
def mergeHourlyResults(hourly_results):
    result = defaultdict(list)  # where the magic happens
    for hres in hourly_results:
        for info in hres:  # info: (etc_entry, etc_exit, avg_travel_time)
            for section, avg_travel_times in info:
                result[section].append(avg_travel_times)
    return result


"""
    return result which has format like:
        { ETC_entry, ETC_exit, 0:00, 0:05, ..., 23:55 }
        NOTE: "0:00" means average travel time at 0:00

"""
def calcDailyTravelTime(date, rootdir):
    path = INPUT_DIR + rootdir+'/' + date
    os.chdir(path)

    hour_dirs = listdirNoHidden('.')
    hourly_results = list(map(calcHourlyTravelTime, hour_dirs))
    result = mergeHourlyResults(hourly_results)  # defaultdcit(list)

    os.chdir('../../../sensor_section')  # back to sensor_section dir
    return result

"""
    Add attribute description and trasnform the dict into list
"""
def transformFormatForOutput(data, date):
    result = []
    result.append(["日期", "測站入口", "測站出口"] + createSensingIntervals(TIME_INTERVAL));
    for section, avg_travel_times in data.items():
        row = [date, section.entry, section.exit] + avg_travel_times
        result.append(row)
    return result

def save(data, dest):
    csv = CSVUtil()
    if not "sensor_section" in os.getcwd():
        print("Not in the sensor_section dir")
        exit(1)
    if not 'output' in os.listdir('.'):
        os.mkdir('output')
    csv.write(data, dest)

def analyze(rootdir, date, save_dest):
    data = calcDailyTravelTime(date, rootdir)
    data = transformFormatForOutput(data, date)
    dest = OUTPUT_DIR + '/' + date + ".csv"
    save(data, save_dest)

def run(arg):
    #slash = lambda p: os.path.join(p, "", "")
    if arg == "batch":
        for rootdir in listdirNoHidden(INPUT_DIR):
            data_dir = INPUT_DIR + rootdir + '/'
            output_dir = OUTPUT_DIR + rootdir + '/'
            if not rootdir in os.listdir(OUTPUT_DIR):
                os.mkdir(output_dir)

            for date in listdirNoHidden(data_dir):
                save_dest = output_dir + date + ".csv"
                analyze(rootdir, date, save_dest)
    elif arg == "test":
        rootdir = "201507"
        date = "20150702"
        save_dest = OUTPUT_DIR + date + ".csv"
        analyze(rootdir, date, save_dest)

### ============= End Main =======================



if __name__ == "__main__":
    args = sys.argv[1:]

    if not "output" in os.listdir('.'):
        os.mkdir("output")

    if not args:
        print('Give me a file name or directory')
        sys.exit(1)
    else:
        for arg in args:
            run(arg)
