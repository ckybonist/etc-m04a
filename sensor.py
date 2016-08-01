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

from config import *
from utils import *


# ====================== MAIN ============================
class Sensor:

    def __init__(self):
        self.__result = []

    def analyze(self):
        calcHour = self.calcHourlyTravelTime
        mergeHours = self.mergeHourlyResults
        save = self.__save
        inputdir = INPUT_DIR
        for anchor_dir in subdirs(inputdir):  # In data/
            for date in subdirs(inputdir + anchor_dir):  # In 201507/
                os.chdir(inputdir + anchor_dir + "/" + date)

                #--------------------------------------------------
                """
                    Daily Travel Time
                        { ETC_entry, ETC_exit, 0:00, 0:05, ..., 23:55 }
                        NOTE: "0:00" means average travel time at 0:00

                """
                hour_dirs = subdirs('.')
                hourly_results = [calcHour(hd) for hd in hour_dirs]
                result = mergeHours(hourly_results)  # OrderedDict(list)
                result = self.formatForOutput(date, result)
                #-----------------------------------------------------

                os.chdir('../../../')  # In data/
                save(anchor_dir, date, result)

    def __save(self, anchor_dir, date, data):
        if "output" not in subdirs('.'):
            os.mkdir("output")

        output_dir = "{}/{}/{}".format(OUTPUT_DIR, "step1", anchor_dir)
        if output_dir not in subdirs(OUTPUT_DIR):
            os.makedirs(output_dir, exist_ok=True)

        #print("OUTPUT: {}".format(os.getcwd()))
        save_dest = "{}/{}".format(output_dir, date + ".csv")
        CSVUtil.save(data, save_dest)

    """  TODO: Need to optimize
        Merge hourly result to daily result (single dictionary)
        {
            SensorSection(entry, exit) : AvergeTravelTime
            ...
        }
    """

    def mergeHourlyResults(self, hourly_results):
        daily_result = OrderedDict()  # where the magic happens
        hourly_results = flatList(flatList(hourly_results))

        for section, avg_times in hourly_results:
            if section not in daily_result:
                daily_result[section] = list()
            else:
                daily_result[section].append(avg_times)

        return daily_result

    def calcHourlyTravelTime(self, hour_dir):
        #print("HOUR_DIR: {}".format(hour_dir))
        calc = self.__calcTravelTimeOfSensorSection
        prefix = "./{}/".format(hour_dir)
        return [calc(prefix + file)
                for file in subfiles(hour_dir)]

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

    def __calcTravelTimeOfSensorSection(self, fname):
        result = []
        c = 0
        weightedTime = 0
        num_cars = 0
        calc = self.__calcTime

        for row in CSVUtil.read(fname):
            c += 1
            weightedTime += int(row[4]) * int(row[5])
            num_cars += int(row[5])
            if c > 0 and c % NUM_CAR_TYPE == 0:
                travel_time = calc(weightedTime, num_cars, row[1], row[2])
                sensor_section = SensorSection(
                    entry=row[1], exit=row[2])  # magic
                result.append((sensor_section, travel_time))
        return result

    def __calcTime(self, weightedTime, num_cars, sid_start, sid_end):
        if num_cars == 0:
            start_pos = getSensorPosition(sid_start)
            end_pos = getSensorPosition(sid_end)
            velocity = 80  # km/h
            hour = 3600
            distance = abs(end_pos - start_pos)
            return hour * math.floor(distance / velocity)  # second
        else:
            return math.floor(weightedTime / num_cars)

    """
        Add attribute description and trasnform the dict into list
    """

    def formatForOutput(self, date, data):
        splitday = splitDay
        interval = TIME_INTERVAL
        time_intervals = splitday(interval)
        header = ["日期", "測站入口", "測站出口"] + time_intervals
        result = [header]

        return[[date, section.entry, section.exit] + avg_times
               for section, avg_times in data.items()]


# ============= End Main =======================

def test():
    from profile import timing, timing2, timing3
    #step1 = Sensor()
    #fn = step1.calcDailyTravelTime
    #fn = step1.calcHourlyTravelTime

    # os.chdir("data/201507/20150702/")
    # os.chdir("data/201507/20150702/")

    #timing2(fn, 1)
    #timing(fn, 72, "00")


if __name__ == "__main__":
    step1 = Sensor()
    fn = step1.analyze
    import time

    print (fn.__name__)
    t1 = time.clock()
    fn()
    # myfunc()
    t2 = time.clock()
    print(round(t2 - t1, 3))
