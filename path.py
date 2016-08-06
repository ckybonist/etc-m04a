#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from config import MYPATHS
from utils import *


class Path:
    targets = []  # target paths

    def __init__(self):
        self.__DATA = []  # travel times of interchange sections
        self.__data_header = []
        self.__DATE = ""

    def test(self):
        anchor = "testing"
        myfile = "20150718.csv"
        step2_dir = "{}/{}/{}".format("output/step2", anchor, myfile)
        self.__readData(step2_dir)
        self.calcTravelTimes()

    def analyze(self):
        pass

    def calcTravelTimes(self):
        for target in Path.targets:
            direction = target[2]
            mydata = self.__filterDataByDirection(direction)
            path = self.__setPath(target[0], target[1], direction)
            start_at = self.__indexOfStartEnd(path, "start", direction, mydata)
            end_at = self.__indexOfStartEnd(path, "end", direction, mydata)
            #self.__debugInterchangesOfPath(path, direction, start_at, end_at, mydata)
            traveltimes = self.__mergeTravelTimes(mydata[start_at : end_at+1])

    def __mergeTravelTimes(self, data):  # TODO
        result = 0.0
        datestr = self.__DATE
        TIMESTAMPS = self.__data_header[4:]
        TIMESTAMPS = [strToDatetimeObj(datestr, timestr) \
                        for timestr in TIMESTAMPS]

        for ia, row in enumerate(data):  # each interchange section
            traveltimes = row[4:]

        return result

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


    def __filterDataByDirection(self, direction):
        predicate = lambda r: r[3] == direction
        return [row for row in self.__DATA if predicate(row)]

    def __readData(self, step2_output_dir):
        #def fn(row):
            # return [row[0],
            #         InterchangeSection(start=row[1], dest=row[2]),
            #         row[3], row[4:]]
        #def fn(row):
            #return [InterchangeSection(start=row[0], dest=row[1]), row[2]]

        data = CSVUtil.read(step2_output_dir)
        self.__DATE = data[1][0]
        self.__data_header = data[0]
        self.__DATA = data[1:]
        Path.targets = MYPATHS
        #self.__DATA = [fn(row) for row in data[1:]]
        #Path.targets = [ fn(row) for row in MYPATHS ]

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
    step3 = Path()
    step3.test()
