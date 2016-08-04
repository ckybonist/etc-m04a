#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
from itertools import groupby, repeat
from functools import cmp_to_key
from utils import *


class Interchange:
    # Class variables
    locations = []
    g_section = []  # for testing

    # Instance methods
    def __init__(self):
        self.path = None
        self.__data = []
        Interchange.locations = CSVUtil.read(
            "resource/mileage_location.csv")[1:]  # remove header

    def analyze(self):
        """
            Caculating travel time of each subpath(interchange section) in path then sum it.
        """
        raw = CSVUtil.read("resource/step1.example.csv")
        self.__refineData(raw)

        # 日期, ..., 方向, 00:00, 00:05, ..., 23:55
        header = [raw[0][0], "上游交流道", "下游交流道", "方向"] + list(raw[0][3:])
        date = raw[1][0]

        result = [header] + self.calcSubPathTravelTime(date)

        saveResult("step2", "20160922", date+".csv", result)

    def calcSubPathTravelTime(self, date):
        locations = Interchange.locations
        lackhead, lacktail = True, False
        result = []


        for group in locations:
            SIZE = len(group)
            myprev, mynext = [], []
            for idx, current in enumerate(group):
                traveltimes = []
                myprev = group[idx-1] if not idx==0 else []
                mynext = group[idx+1] if not idx==SIZE-1 else []

                if not myprev:
                    traveltimes = self.__calcTimesBySingleSection(current, myprev, mynext, lackhead)
                elif not mynext:
                    traveltimes = self.__calcTimesBySingleSection(current, myprev, mynext, lacktail)
                else:
                    traveltimes = self.__calcSubPath(current, myprev, mynext)

                header = [date, current[1], current[2], current[0][-1]]
                traveltimes = [ round(float(time)) for time in traveltimes ]
                result.append(header + traveltimes)

        return result


    def __calcSubPath(self, current, myprev, mynext):
        loc_up_ic = current[3]
        loc_down_ic = current[4]
        lackhead, lacktail = True, False
        direction = current[0][-1]
        result = []

        head_travel_times = self.__calcHead(myprev[0], current[0], loc_up_ic)
        tail_travel_times = self.__calcTail(current[0], mynext[0], loc_down_ic)
        both_times = head_travel_times + tail_travel_times

        if not head_travel_times:
            result = self.__calcTimesBySingleSection(current, myprev, mynext, lackhead)
        elif not tail_travel_times:
            result =  self.__calcTimesBySingleSection(current, myprev, mynext, lacktail)
        elif not both_times:  # can't get travel times of both sensor sections
            N = (24 * 60) / TIME_INTERVAL - 1
            DEFAULT_TRAVLE_TIME = abs(current[4] - current[3]) / DEFAULT_SPEED
            result = [DEFAULT_TRAVLE_TIME] * N
        else:
            result = mappedList(operator.add, head_travel_times, tail_travel_times)

        return result

    def __calcTimesBySingleSection(self, cur, myprev, mynext, lackhead=True):
        """ Caculate travel time of interchange section in some special cases.

            Speical cases: For cases that lack either travel time of sensor section
                           i.e. no sensor behind(after) the upstream(downstream) interchange.

            Args:
                @cur: current location record
                @myprev: previous location record
                @mynext: next location record
                @lackhead -> boolean: lack of travel time of head sensor section

            Returns:
                A list of float numbers, each element indicates travel time which
                detected at specific timestamp. For example:

                00:00 00:05 00:10 ... 23:55 <--- for explanation
                [231, 145, 281, ..., 152]   <--- 288 elements


            NOTE: "Location" means mileage of each sensors and interchages.
        """
        loc_up_ic = cur[3]
        loc_down_ic = cur[4]
        cur_sensor_id = cur[0]
        traveltimes = []
        ratio = self.__calcSensorRatio(loc_up_ic, loc_down_ic, cur_sensor_id)  # head ratio

        if lackhead and mynext:
            traveltimes = self.__calcTail(cur_sensor_id, mynext[0], loc_down_ic)
        elif not lackhead and myprev:
            traveltimes = self.__calcHead(myprev[0], cur_sensor_id, loc_up_ic)
            ratio = 1 - ratio

        if ratio == 0.0:
            print("head or tail ratio is 0: {}, {}".format(cur[1], cur[2]))

        return [ time + time*ratio
                 for time in traveltimes ]

    def __calcHead(self, prev_sensor_id, cur_sensor_id, loc_up_ic):
        """ Caculate travel time of left-part in interchange section

            Args:
                @prev_sensor_id: ID of sensor behind the one in current interchange section
                @cur_sensor_id: ID of sensor in current interchange section
                @loc_up_ic: Location(mileage) of current upstream interchange

            Returns:
                A list of travel time
                    or
                Empty list
        """
        direction = cur_sensor_id[-1]
        section = self.__createSensorSection(prev_sensor_id, cur_sensor_id)
        traveltimes = self.__getSensorSectionTravelTimes(section)

        if not traveltimes:
            if Interchange.g_section != section:
                Interchange.g_section = section
                print("{},{}".format(section[0], section[1]))
            return []
        ratio = self.__calcInterchangeRatio(loc_up_ic, section, upstream_interchange=True)

        return [ ratio * t for t in traveltimes ]


    def __calcTail(self, cur_sensor_id, next_sensor_id, loc_down_ic):
        """ Caculate travel time of right-part in interchange section

            Args:
                @cur_sensor_id: ID of sensor in current interchange section
                @next_sensor_id: ID of sensor after the current sensor
                @loc_down: Location(mileage) of current downstream interchange

            Returns:
                A list of travel time
                    or
                Empty list
        """
        direction = cur_sensor_id[-1]
        section = self.__createSensorSection(cur_sensor_id, next_sensor_id)
        traveltimes = self.__getSensorSectionTravelTimes(section)

        if not traveltimes:
            if Interchange.g_section != section:
                Interchange.g_section = section
                print("{},{}".format(section[0], section[1]))
            return []
        ratio = self.__calcInterchangeRatio(loc_down_ic, section, upstream_interchange=False)

        return [ ratio*time for time in traveltimes ]


    def __refineData(self, raw_data):
        """
            Refine step1 data (output/step1/*/*.csv)

            Result:
                [ Date, SensorSection(entry, exit), [t_0000, t_0005, t_0010, ..., t_2355] ]

            @direction: 'N' or 'S'
        """
        def fn1(row):
            return [row[0],
                    SensorSection(entry=row[1], exit=row[2]),
                    row[3:]]
        self.__data = [fn1(r) for r in raw_data[1:]]

        def fn2(row):
            head = list(row[:3])
            tail = floatList(row[3:])
            return head + tail
        locations = Interchange.locations
        locations = sorted(locations, key=lambda e: e[0][-1])
        Interchange.locations = [ fn2(r) for r in locations ]
        self.__separateInterchange()

    def __separateInterchange(self):
        locations = Interchange.locations
        Interchange.locations = [ list(g) for _, g in groupby(locations, lambda e: e[0][:3]) ]


    def __constructSSIDs(self):
        """
            將所有測站ID 轉為測站區間
            例如：
                原始是 ['A', 'B', 'C', 'D'] 四個測站ID
                轉換後為 [ ('A', 'B'), ('B', 'C'), ('C', 'D') ]
                最後再把每一個元素轉型為 SectionSensor (see config.py)
        """
        ssids = [ e[0] for e in Interchange.locations ]
        ssids = list(zip(ssids, ssids[1:]))
        return ssids


    def __calcInterchangeRatio(self, loc_interchange, sensor_section, upstream_interchange=True):
        sub_delta = 0  # distance between sensor and interchange

        direction = sensor_section[0][-1]
        if direction == 'N':
            sensor_section = self.__swapSensorIdsOfSection(sensor_section)

        delta, loc_sensor_start, loc_sensor_end = \
                getDistanceOfSensorSection(sensor_section)

        if upstream_interchange:
            sub_delta = loc_sensor_end - loc_interchange
        else:
            sub_delta = loc_interchange - loc_sensor_start


        return abs(sub_delta / delta)

    def __calcSensorRatio(self, loc_up_ic, loc_down_ic, sensor_id):
        """
            Ratio between iterchange and sensor, defualt result is the ratio of
            distance between "upstream interchange" and sensor.
        """
        loc_sensor = getSensorLocation(sensor_id)
        return abs(loc_sensor - loc_up_ic) / abs(loc_down_ic - loc_up_ic)

    def __createSensorSection(self, start_id, end_id):
        dir_a, dir_b = start_id[-1], end_id[-1]

        if dir_a == 'N' and dir_b == 'N':
            return SensorSection(entry=end_id, exit=start_id)
        elif dir_a == 'S' and dir_b == 'S':
            return SensorSection(entry=start_id, exit=end_id)
        else:
            print("Error when creating section")

    def __swapSensorIdsOfSection(self, section):
        myentry, myexit = section[1], section[0]
        return SensorSection(entry=myentry, exit=myexit)


    def __getSensorSectionTravelTimes(self, sensor_section):
        """
            Return all-day-long travel times of given sensor section.
        """
        for row in self.__data:
            if row[1] == sensor_section:
                return floatList(row[2])


    def __findInterchangeLocation(self, interchange):
        """
            Retrun location(mileage) of the interchange

            @interchange: name of interchange
        """
        for row in Interchange.locations:
            try:
                idx = row.index(interchange)
                return float(row[idx + 2])
            except ValueError:
                continue



if __name__ == "__main__":
    step2 = Interchange()
    step2.analyze()
