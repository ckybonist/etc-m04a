#!/usr/bin/env python
# -*- coding: utf-8 -*-


from utils import *


class Interchange:
    # Class variables
    locations = []

    # Instance methods
    def __init__(self):
        self.path = None
        self.__data = []
        Interchange.locations = CSVUtil.read(
            "resource/etc-sensor-loc.csv")[1:]  # remove header

    """
        Caculating travel time of each subpath(interchange section) in path then sum it.
    """

    def analyze(self):
        raw = CSVUtil.read("resource/sensor_section.example.csv")
        header = raw[0]
        timestamps = header[3:]
        result = [header]
        self.__refineData(raw)
        result = self.calcSubPathTravelTime()

        for r in result:
            print(r[2])  # 00:10


    # BUG: Error occurs in 01F2866S (due to no this sensor record in training data)
    def calcSubPathTravelTime(self):
        locations = Interchange.locations
        result = []
        enum = enumerate(locations)
        for idx, current in enum:
            if current[3] == 0:  # upstream interchange's location is 0 km.
                pass
            else:
                prev = locations[idx-1]
                next = locations[idx+1]
                section1 = SensorSection(entry=prev[0], exit=current[0])
                section2 = SensorSection(entry=current[0], exit=next[0])

                ratio1 = self.__calcRatio(current[3], prev[-1], current[-1], upstream_interchange=True)
                ratio2 = self.__calcRatio(current[3], current[-1], next[-1], upstream_interchange=False)

                calc = lambda t1, t2: ratio1 * t1 + ratio2 * t2
                time_lst1 = self.__getSensorSectionTravelTimes(section1)
                time_lst2 = self.__getSensorSectionTravelTimes(section2)
                if not time_lst2:
                    print(current)
                times = zip(time_lst1, time_lst2)

                traveltimes = [ calc(t1, t2) for t1, t2 in times ]
                subpath = (current[1], current[2], traveltimes)
                result.append(subpath)

        return result



    """
        Refine step1 data (output/step1/*/*.csv)

        Result:
            [ Date, SensorSection(entry, exit), [t_0000, t_0005, t_0010, ..., t_2355] ]

        @direction: 'N' or 'S'
    """

    def __refineData(self, raw_data):
        def fn1(row):
            return [row[0],
                    SensorSection(entry=row[1], exit=row[2]),
                    row[3:]]
        self.__data = [fn1(r) for r in raw_data[1:]]

        def fn2(row):
            head = list(row[0:3])
            tail = floatList(row[3:])
            return head + tail
        Interchange.locations = [ fn2(r) for r in Interchange.locations ]


    """
        將所有測站ID 轉為測站區間
        例如：
            原始是 ['A', 'B', 'C', 'D'] 四個測站ID
            轉換後為 [ ('A', 'B'), ('B', 'C'), ('C', 'D') ]
            最後再把每一個元素轉型為 SectionSensor (see config.py)
    """
    def __constructSSIDs(self, entry, exit):
        ssids = [ e[0] for e in Interchange.locations ]
        ssids = list(zip(ssids, ssids[1:]))
        return ssids


    def __calcRatio(self, loc_interchange, loc_sensor_start, loc_sensor_end, upstream_interchange=True):
        delta = abs(loc_sensor_end - loc_sensor_start)  # distance of sensor section
        sub_delta = 0  # distance between sensor and interchange
        if upstream_interchange:
            sub_delta = loc_sensor_end - loc_interchange
        else:
            sub_delta = loc_interchange - loc_sensor_start

        return sub_delta / delta


    def __getSensorSectionTravelTimes(self, sensor_section):
        for row in self.__data:
            if row[1] == sensor_section:
                return floatList(row[2])

    """
        Retrun location(mileage) of the interchange

        @interchange: name of interchange
    """

    def __findInterchangeLocation(self, interchange):
        for row in Interchange.locations:
            try:
                idx = row.index(interchange)
                return float(row[idx + 2])
            except ValueError:
                continue



if __name__ == "__main__":
    step2 = Interchange()
    step2.analyze()
