#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time as systime
import datetime
from collections import defaultdict

from config import MYPATHS, MISSING_TOMORROW
from utils import *


class Path:
    targets = []  # target paths

    def __init__(self):
        self.__DATE = ""
        self.__DATA = []  # step2 data
        self.__NEXTDAY_DATA = []  # step2 data
        self.__DATA_HEADER = []
        self.__TIMESTAMPS = []
        self.__ANCHOR_TABLE = defaultdict()  # key: day, value: anchor
        self.__generateAnchorTable("output/step2/")  # do not omit last slash

    def test(self):
        anchor = "20160820"
        myfile = "20150718.csv"
        data_path = "{}/{}/{}".format("output/step2", anchor, myfile)
        self.__readData(data_path)
        self.calcTravelTimes()

    def analyze(self):
        rootdir = "output/step2/"
        for anchor in subdirs(rootdir):
            subdir = rootdir + anchor
            for myfile in subfiles(subdir):
                if myfile in MISSING_TOMORROW:
                    continue
                print(myfile)
                data_path = "{}/{}".format(subdir, myfile)
                self.__readData(data_path)
                result = self.calcTravelTimes()
                saveResult("step3", anchor, self.__DATE+".csv", result)

    def calcTravelTimes(self):
        """ Caculate travel times of all paths """
        result = [self.__DATA_HEADER]
        for target in Path.targets:
            direction = target[2]
            #print("================")
            #print(target[0], target[1])
            traveltimes = self.__mergeTravelTimesOfPath(direction, target)
            row = [self.__DATE] + list(target)
            row.extend(traveltimes)
            result.append(row)
        return result

    def __mergeTravelTimesOfPath(self, direction, target_path):  # TODO: too slow
        """ Return list of path travel times which start at each timestamp """
        data = self.__filterData(target_path, direction, is_tomorrow=False)
        result = []

        def calcTimeForEachTimestamp(time_idx, timestamp):
            """ Return travel time of the path at given timestamp """
            result_time = 0
            cur_time = timestamp

            for idx, subpath in enumerate(data):
                traveltimes = list(subpath[4:])
                traveltime = int(traveltimes[time_idx])
                cur_time += timeDelta(traveltime, "seconds")
                if idx > 0 and cur_time > timestamp:
                    minute = cur_time.minute - (cur_time.minute % TIME_INTERVAL)  # e.g. 43 to 40
                    dt = cur_time
                    dt = dt.replace(minute = minute, second = 0)
                    if cur_time.date() > timestamp.date():  # next day
                        traveltimes = self.__getTomorrowTravelTimes(target_path, subpath[1:4])
                    time_idx = self.__getIndexOfTime(dt)
                    #time_idx = self.__TIMESTAMPS.index(dt)
                result_time += int(traveltimes[time_idx])
            return result_time

        result = [calcTimeForEachTimestamp(idx, timestamp) \
                    for idx, timestamp in enumerate(self.__TIMESTAMPS)]
        return result

    def __getIndexOfTime(self, cur_time):
        hour = int(cur_time.hour)
        minute = int(cur_time.minute)
        intervals_in_hour = 60 / TIME_INTERVAL
        result = hour * intervals_in_hour + (minute / TIME_INTERVAL + 1)
        return int(result) - 1

    def __getTomorrowTravelTimes(self, target_path, subpath):
        """ Return travel of specific interchange section in record of given date

            Args:
                @date: datetime.date object; the date of record(data)
                @subpath: (upstream_interchange, downstream_interchange, direction)

            Note: Ics(ICS) is short for InterChangeSection
        """
        direction = subpath[2]
        data = self.__filterData(target_path, direction, is_tomorrow=True)
        traveltimes = next(row for row in data if row[1:4] == subpath)[4:]
        return traveltimes

    def __filterData(self, target, direction, is_tomorrow=False):
        raw_data = self.__DATA
        if is_tomorrow:
            raw_data = self.__NEXTDAY_DATA

        data = self.__filterDataByDirection(direction, raw_data)
        path = self.__setPath(target[0], target[1], direction)
        start_at = self.__indexOfStartEnd(path, "start", direction, data)
        end_at = self.__indexOfStartEnd(path, "end", direction, data)
        #self.__debugInterchangesOfPath(path, direction, start_at, end_at, data)
        return data[start_at : end_at+1]

    def __setPath(self, start, end, direction):
        if direction == "N" :
            start, end = end, start
        return (start, end)

    def __indexOfStartEnd(self, path, flag, direction, data):
        start, end = path

        def pred_x(row):  # match start/end point of path in data
            idx_ic = 1 if flag=="start" else 2
            interchange = start if flag=="start" else end
            return interchange == row[idx_ic] and direction == row[3]

        def pred_y(idx):  # filter out the interchange which not in path
            if path == ("南港系統", "蘇澳") and flag == "start":
                return data[idx][2] == "石碇"
            elif path == ("圓山", "新竹系統") and flag == "end":
                return data[idx][1] == "新竹(園區二路)"
            else:
                return True

        index = [ idx for idx, row in enumerate(data) \
                    if pred_x(row) and pred_y(idx) ]

        if len(index) > 1:
            print("Error: we should only have one start or end point")
            print(index)
            sys.exit(1)
        else:
            index = index[0]

        return index


    def __filterDataByDirection(self, direction, data):
        predicate = lambda r: r[3] == direction
        return [row for row in data if predicate(row)]

    def __updateTimeStamps(self, date):
        if isinstance(date, datetime.date):
            date = date.strftime("%Y%m%d")
        self.__TIMESTAMPS = self.__DATA_HEADER[4:]
        self.__TIMESTAMPS = [strToDatetimeObj(date, timestr) \
                                for timestr in self.__TIMESTAMPS]

    def __readData(self, data_path):
        # Today
        data = CSVUtil.read(data_path)
        self.__DATE = data[1][0]
        self.__DATA_HEADER = data[0]
        self.__DATA = data[1:]

        # Tomorrow
        def inc_day(datestr):
            fmt = "%Y%m%d"
            mydate = datetime.datetime.strptime(datestr, fmt) + timeDelta(1, "days")
            return mydate.strftime(fmt)

        tomorrow = inc_day(self.__DATE) + ".csv"
        anchor = self.__ANCHOR_TABLE[tomorrow]
        path = "output/step2/{}/{}".format(anchor, tomorrow)
        self.__NEXTDAY_DATA = CSVUtil.read(path)[1:]

        #Path.targets = [MYPATHS[0]]
        Path.targets = MYPATHS

        self.__updateTimeStamps(self.__DATE)

    def __generateAnchorTable(self, mydir):
        for anchor in subdirs(mydir):
            for day in subfiles(mydir + anchor):
                self.__ANCHOR_TABLE[day] = anchor

    def __debugInterchangesOfPath(self, path, direction, start_at, end_at, mydata):
        print("===========================")
        print(path, direction)
        print("{}, {}".format(start_at, end_at))
        ia, ib = start_at, end_at
        print("{}, {}".format(mydata[ia][1], mydata[ia][2]), mydata[ia][3])
        print("{}, {}".format(mydata[ib][1], mydata[ib][2]), mydata[ia][3])
        print("===========================\n")


# End of Path

if __name__ == "__main__":
    t1 = systime.clock()
    step3 = Path()
    #step3.test()
    step3.analyze()
    t2 = systime.clock()
    print("Exec time of program: {}".format(round(t2-t1, 3)))
