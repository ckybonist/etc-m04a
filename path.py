#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from config import MYPATHS
from utils import CSVUtil, InterchangeSection


class Path:
    targets = []  # target paths

    def __init__(self):
        self.__data = []  # travel times of interchange sections
        self.__data_header = []
        self.__DATE = ""

    def test(self):
        anchor = "20160820"
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
            start, end = target[0], target[1]
            if direction == "N":
                start, end = target[1], target[0]
            print(start, end, direction)
            self.__indexOfElement(start, direction, mydata, is_start=True)
            #print(start_at, end_at)

    def __indexOfElement(self, interchange, direction, data, is_start=True):
        def predicate(row):
            idx_ic = 1 if is_start else 2
            return interchange == row[idx_ic] and direction == row[3]

        tmp = [ idx for idx, row in enumerate(data) if predicate(row) ]
        print(tmp)

    def __filterDataByDirection(self, direction):
        predicate = lambda r: r[3] == direction
        return [row for row in self.__data if predicate(row)]

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
        self.__data = data[1:]
        Path.targets = MYPATHS
        #self.__data = [fn(row) for row in data[1:]]
        #Path.targets = [ fn(row) for row in MYPATHS ]

# End of Path

if __name__ == "__main__":
    step3 = Path()
    step3.test()
