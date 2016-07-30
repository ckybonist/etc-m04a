#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Average travel time of sensor sections:

    Input Data: TDCS_M04A_[date]_[time]

    Data Format:
        row[0], row[1], row[2], row[3], row[4], row[5]
        date_time,  etc_entrance, etc_exit, car_type, mean_travel_time, num_cars
"""

import os
import sys
import math
from collections import OrderedDict

from config import Config
from utils import SensorSection, CSVUtil, createSensingIntervals, listdirNoHidden



### ====================== MAIN ============================
class Sensor:
    def __init__(self):
        pass




""" TODO: UGLY CODE
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
def calc(fname):
    def myFn(weightedTime, num_cars, sid_start, sid_end):
        result = 0.0
        if num_cars == 0:
            start_pos = getSensorPosition(sid_start)
            end_pos = getSensorPosition(sid_end)
            distance = abs(end_pos - start_pos)
            velocity = 80  # km/h
            result = math.floor(distance / velocity) * 3600  # second
        else:
            result =  math.floor(weightedTime / num_cars)
        return result


    data = CSVUtil.read(fname)
    c = 0
    weightedTime = 0
    num_cars = 0
    result = []

    for row in data:
        c += 1
        weightedTime += int(row[4]) * int(row[5])
        num_cars += int(row[5])
        if c > 0 and c % NUM_CAR_TYPE == 0:
            travel_time = myFn(weightedTime, num_cars, row[1], row[2])
            sensor_section = SensorSection(entry=row[1], exit=row[2])  # magic
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
        result.append(calc(f))
    return result

"""
    Merge hourly result to daily result (single dictionary)
    {
        SensorSection(entry, exit) : AvergeTravelTime
        ...
    }
"""
def mergeHourlyResults(hourly_results):
    result = OrderedDict()  # where the magic happens
    for res in hourly_results:
        for info in res:  # info: (etc_entry, etc_exit, avg_travel_time)
            for section, avg_travel_times in info:
                if section not in result:
                    result[section] = list()
                else:
                    result[section].append(avg_travel_times)
    return result

def debug_xs(obj):
    for i, e in enumerate(obj):
        if i == 3:
            break
        else:
            print(e)
            i += 1

def debug_dict(obj):
    i = 0
    for k, v in obj.items():
        if i == 3:
            break
        else:
            print("{} -> {}".format(k, v))
            i+=1

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
    result = mergeHourlyResults(hourly_results)  # OrderedDict(list)

    os.chdir('../../../')  # back to root dir

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

def handleDirPath(rootdir):
    data_dir = INPUT_DIR + rootdir + '/'
    output_dir = OUTPUT_DIR + rootdir + '/'
    if not rootdir in os.listdir(OUTPUT_DIR):
        os.mkdir(output_dir)

def run(arg):
    #slash = lambda p: os.path.join(p, "", "")
    listDir = listdirNoHidden

    for rootdir in listDir(INPUT_DIR):
        handleDirPath(rootdir)
        for date in listDir(data_dir):
            save_dest = output_dir + date + ".csv"
            #analyze(rootdir, date, save_dest)
            result = calcDailyTravelTime(date, rootdir)
            result = transformFormatForOutput(result, date)
            CSVUtil.save(result, save_dest)

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

    rootdir = "201507"
    date = "20150702"
    save_dest = OUTPUT_DIR + date + ".csv"
    analyze(rootdir, date, save_dest)
