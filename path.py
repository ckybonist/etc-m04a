#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Path:
    def __init__(self):
        pass

    def calcTravelTimesOfPath(self, path, step1_data_path):
        self.path = path
        direction = path[2]
        raw_data = CSVUtil.read("resource/sensor_section.example.csv")[1:]

        self.__refineData(direction, raw_data)
        routes = self.__listSensorSectionsOfPath(
            path, direction)  # sensor sections of path

        pass

    """ TODO: Refine code
        記錄路徑中所有的測站區間
    """
    def __listSensorSectionsOfPath(self, path, direction):
        sections = []
        flag = False
        start, end = (path[0], path[1]) if direction == '南'
                                        else (path[1], path[0])

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
            sections = [SensorSection(entry=x, exit=y) for x, y in sections]
        else:
            sections = [SensorSection(entry=y, exit=x) for x, y in sections]

        return sections

    def __filterDataByDirection(self, direction, raw_data):
        def myFilter(pred, xs):
            return [e for e in xs if pred(e, dire)]

        def pred_a(e, d):
            return e[1][-1] == d and e[2][-1] == d

        def pred_b(e, d):
            return e[0][-1] == d

        result = []
        xs = []
        predicate = None
        dire = 'S' if direction == "南" else 'N'

        self.__data = myFilter(pred_a, raw_data)

        self.__sensor_locations = myFilter(
            pred_b, Interchange.SENSOR_LOCATIONS)

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

    def __refineData(self, direction, raw_data):
        self.__filterDataByDirection(direction, raw_data)

        def fn(e):
            return [e[0],
                    SensorSection(entry=e[1], exit=e[2]),
                    e[3:]]

        self.__data = [fn(e) for e in self.__data]

# End of Path

if __name__ == "__main__":
    pass
