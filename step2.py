#!/usr/bin/env python
# -*- coding: utf-8 -*-


from config import SensorSection
from utils import *


class Analyzer:
    def __init__(self):
        self.SENSOR_LOCATIONS = CSVUtil.read("resource/etc-sensor-loc.csv")[1:]
        self.DATA = CSVUtil.read("resource/sensor_section.example.csv")[1:]
        self.path = None
        self.__data = []
        self.__sensor_locations = []

    """
        Estimated travel times of paths which sum by
        sensor sections.
    """
    def run(self, paths):
        return [ self.calcTravelTimes(path) for path in paths ]

    def calcTravelTimes(self, path):
        self.path = path
        result = []
        direction = path[2]

        self.__refineData(direction)
        routes = self.__getSensorSectionsOfPath(path, direction)  # sensor sections of path

        return self.__mergeTravelTimeOfSensorSections(routes)


    def __mergeTravelTimeOfSensorSections(self, routes):
        first_times, final_times = self.__getBothEndsSubSectionTravelTime(routes)
        middle_times = self.__getMiddleEndSubSectionTravelTime(routes)

        result = mappedList(sum, zip(first_times, middle_times, final_times))
        result = mappedList(round, result)

        return result

    def __getMiddleEndSubSectionTravelTime(self, routes):
        # filter the sensor sections which not in path
        middle_times = [ d[2] for d in self.__data \
                            for r in routes[1:-1] \
                            if d[1] == r ]
        # merge all sensor sections into one element
        middle_times = list(zip(*middle_times))

        # travel_times of path's middle part
        middle_times = [ sumMappedList(float, times) for times in middle_times ]

        return middle_times

    """
        Refine data and sensor-locations-records:
        For data:
            - filter by direction
            - merge two sensor ids into SensorSection type
        For sensor-locations-records:
            - filter by direction

        Result:
            [ Date, SensorSection, [travel_times_at_each_timestamp...] ]

        @direction: 'N' or 'S'
    """
    def __refineData(self, direction):
        self.__filterDataByDirection(direction)
        fn = lambda e: [ e[0], SensorSection(entry=e[1], exit=e[2]), e[3:] ]
        self.__data = [ fn(e) for e in self.__data ]


    """ TODO: Refine code
        記錄路徑中所有的測站區間
    """
    def __getSensorSectionsOfPath(self, path, direction):
        sections = []
        flag = False
        start, end = (path[0], path[1]) \
                if direction == '南' else (path[1], path[0])

        for row in self.__sensor_locations:
            if row[2] == start:
                flag = True

            if flag:
                sections.append(row[0])

            if row[1] == end:
                break
        """
            magic: 將所有測站ID 轉為測站區間
            例如：
                原始是 ['A', 'B', 'C', 'D'] 四個測站ID
                轉換後為 [ ('A', 'B'), ('B', 'C'), ('C', 'D') ]
                最後再把每一個元素轉型為 SectionSensor (see config.py)
        """
        sections = list(zip(sections, sections[1:]))
        if direction == '南':
            sections = [ SensorSection(entry=x, exit=y) for x,y in sections ]
        else:
            sections = [ SensorSection(entry=y, exit=x) for x,y in sections ]

        return sections

    """
        Return travel time of first and final sub-section.
        Sub-section means the section between interchange and sensor, so:
            first sub-section means:
                start point of path <---> sensor  (right hand side has larger mileage)
            final sub-section means:
                sensor <---> end point of path

        @routes: Sensor sections of path
    """
    def __getBothEndsSubSectionTravelTime(self, routes):
        start, end = routes[0], routes[-1]
        #print(start, end)

        #------------------- TODO: UGLY CODE --------------------------
        first_times = self.__getSensorSectionTravelTime(start)
        final_times = self.__getSensorSectionTravelTime(end)
        #-------------------- TODO ------------------------------------
        first_prop, last_prop = self.__getBothEndsProportions(routes)

        first_times = [ float(t) * first_prop for t in first_times ]
        final_times = [ float(t) * last_prop for t in final_times ]

        return first_times, final_times


    """
        算出路徑中第一個(最後一個)交流道 到 下一個(上一個) 測站
        的距離在其測站區間所佔的比例 (也就是這兩個子路段所佔的比例)

        @start: 起點交流道名稱
        @end: 終點交流道名稱
        @return: Tuple; (初始子路段比例, 最後子路段比例)
    """
    def __getBothEndsProportions(self, routes):
        def toFloat(xs):
            result = list(xs[:3])
            result.extend([float(e) for e in xs[3:]])
            return result

        pa = self.__getFirstEndProportion(routes[0])
        pb = self.__getFinalEndProportion(routes[-1])

        return pa, pb


    def __getFirstEndProportion(self, sensor_section):
        d1 = getDistanceOfSensorSection(sensor_section)  # section distance

        pos_ic = self.__findInterchangePosition(self.path[0])  # start interchange position
        pos_se = getSensorPosition(sensor_section[1])  # end sensor position
        d2 =  pos_se - pos_ic

        #return round(d2 / d1, 3)  # for testing
        return d2 / d1

    def __getFinalEndProportion(self, sensor_section):
        d1 = getDistanceOfSensorSection(sensor_section)

        pos_ie = self.__findInterchangePosition(self.path[1])  # end interchange postition
        pos_ss = getSensorPosition(sensor_section[0])  # starting sensor position
        d2 = pos_ie - pos_ss

        #return round(d2 / d1, 3)  # for testing
        return d2 / d1


    def __getSensorSectionTravelTime(self, section):
        for row in self.__data:
            if row[1] == section:
                return row[2]

    """
        Retrun location(mileage) of the interchange

        @interchange: name of interchange
    """
    def __findInterchangePosition(self, interchange):
        for row in self.__sensor_locations:
            try:
                idx = row.index(interchange)
                return float(row[idx + 2])
            except ValueError:
                continue


    def __filterDataByDirection(self, direction):
        result = []
        xs = []
        predicate = None

        dire = 'S' if direction == "南" else 'N'

        def myFilter(pred, xs):
            return [ e for e in xs if pred(e, dire) ]

        pred_a = lambda e, d: e[1][-1] == d and e[2][-1] == d
        self.__data = myFilter(pred_a, self.DATA)

        pred_b = lambda e, d: e[0][-1] == d
        self.__sensor_locations = myFilter(pred_b, self.SENSOR_LOCATIONS)



if __name__ == "__main__":
    from path import PATHS

    obj = Analyzer()
    TEST_PATH = [PATHS[3]]
    ACTUAL_TRAVEL_TIME = 738

    result = obj.run(TEST_PATH)
    assert(ACTUAL_TRAVEL_TIME == guess[1])  # check path-4's travel time which start at 00:05
