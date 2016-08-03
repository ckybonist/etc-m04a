#!/usr/bin/env python
# -*- coding: utf-8 -*-


import operator
from itertools import groupby
from utils import *


class Interchange:
    # Class variables
    locations = []

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
        header = raw[0]
        timestamps = header[3:]
        result = [header]
        self.__refineData(raw)
        result = self.calcSubPathTravelTime()

        #print("{} <--> {} : {}".format(result[0][0], result[0][1], result[0][:5]))


    def calcSubPathTravelTime(self):
        locations = Interchange.locations
        for_head, for_tail = True, False
        result = []

        for grp in locations:
            SIZE = len(grp)
            for idx, current in enumerate(grp):
                traveltimes = []
                myprev = grp[idx-1]
                mynext = grp[idx+1]

                if idx == 0:
                    traveltimes = self.__calcSpecialCase(current, myprev, mynext, for_head)
                elif idx == SIZE-1:
                    traveltimes = self.__calcSpecialCase(current, myprev, mynext, for_tail)
                else:
                    traveltimes = self.__calcSubPath(current, myprev, mynext)

                traveltimes = mappedList(float, traveltimes)
                result.append([current[1], current[2] + traveltimes)

        return result


    def __calcSubPath(self, current, myprev, mynext):
        cur_sensor_id = current[0]
        prev_sensor_id = myprev[0]
        next_sensor_id = mynext[0]
        loc_up_ic = current[3]
        loc_down_ic = current[4]

        head_travel_times = self.__calcHead(prev_sensor_id, cur_sensor_id, loc_up_ic)
        tail_travel_times = self.__calcTail(cur_sensor_id, next_sensor_id, loc_down_ic)

        if head_travel_times

        return mappedList(operator.add, head_travel_times, tail_travel_times)


    def __calcSpecialCase(self, cur, myprev, mynext, lackhead=True):
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
        prev_sensor_id = myprev[0]
        next_sensor_id = mynext[0]

        travel_times = self.__calcTail(cur_sensor_id, next_sensor_id, loc_down_ic) if lackhead else \
                       self.__calcHead(prev_sensor_id, cur_sensor_id, loc_up_ic)

        ratio = self.__calcRatioOfSensorLoc(loc_up_ic, loc_down_ic, cur_sensor_id)  # head ratio
        ratio = (1 - ratio) if not lackhead else ratio

        return [ time + time*ratio
                 for time in travel_times ]

    def __calcHead(self, prev_sensor_id, cur_sensor_id, loc_up_ic):
        """ Caculate travel time of left-part in interchange section

            Args:
                @prev_sensor_id: ID of sensor behind the one in current interchange section
                @cur_sensor_id: ID of sensor in current interchange section
                @loc_up_ic: Location(mileage) of current upstream interchange

            Returns:
                A list of travel time
                    or
                -1 (if travel times of given sensor section not found)
        """
        section = SensorSection(entry=prev_sensor_id, exit=cur_sensor_id)
        travel_times = self.__getSensorSectionTravelTimes(section)
        if not travel_times:
            print("Travel times of {} not found".format(section))
            return []

        ratio = self.__calcRatioOfICLoc(loc_up_ic, section, upstream_interchange=True)

        return [ ratio * t for t in travel_times ]

    def __calcTail(self, cur_sensor_id, next_sensor_id, loc_down_ic):
        """ Caculate travel time of right-part in interchange section

            Args:
                @cur_sensor_id: ID of sensor in current interchange section
                @next_sensor_id: ID of sensor after the current sensor
                @loc_down: Location(mileage) of current downstream interchange

            Returns:
                A list of travel time
                    or
                -1 (if travel times of given sensor section not found)
        """
        section = SensorSection(entry=cur_sensor_id, exit=next_sensor_id)
        travel_times = self.__getSensorSectionTravelTimes(section)
        if not travel_times:
            print("Travel times of {} not found".format(section))
            return []

        ratio = self.__calcRatioOfICLoc(loc_down_ic, section, upstream_interchange=False)

        return [ ratio * t for t in travel_times ]


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
        Interchange.locations = [ fn2(r) for r in Interchange.locations ]
        self.__separateInterchange()

    def __separateInterchange(self):
        locations = Interchange.locations
        Interchange.locations = [ list(g) for _, g in groupby(locations, lambda e: e[0][:3]) ]


    def __constructSSIDs(self, entry, exit):
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


    def __calcRatioOfICLoc(self, loc_interchange, sensor_section, upstream_interchange=True):
        loc_sensor_start = getSensorLocation(sensor_section[0])
        loc_sensor_end = getSensorLocation(sensor_section[1])
        delta = getDistanceOfSensorSection(sensor_section)
        sub_delta = 0  # distance between sensor and interchange

        if upstream_interchange:
            sub_delta = loc_sensor_end - loc_interchange
        else:
            sub_delta = loc_interchange - loc_sensor_start

        return sub_delta / delta

    def __calcRatioOfSensorLoc(self, loc_up_ic, loc_down_ic, sensor_id):
        """
            Ratio between iterchange and sensor, defualt result is the ratio of
            distance between "upstream interchange" and sensor.
        """
        loc_sensor = getSensorLocation(sensor_id)
        return abs(loc_sensor - loc_up_ic) / abs(loc_down_ic - loc_up_ic)



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
