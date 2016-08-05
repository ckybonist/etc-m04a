#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import MYPATHS
from utils import CSVUtil, InterchangeSection


class Path:
    targets = []  # target paths

    def __init__(self):
        self.__data = []  # travel times of interchange sections
        self.__data_header = []

    def test(self):
        anchor = "20160820"
        myfile = "20150718.csv"
        step2_dir = "{}/{}/{}".format("output/step2", anchor, myfile)
        self.__readData(step2_dir)

        print(self.__data_header)
        for target in Path.targets:
            direction = target[1]
            mydata = self.__filterDataByDirection(direction)
            for row in mydata:
                print(row)

    def analyze(self):
        pass

    def calcTravelTimes(self, path, step1_data_path):
        self.path = path
        direction = path[2]
        raw_data = CSVUtil.read("resource/sensor_section.example.csv")[1:]

        self.__refineData(direction, raw_data)
        routes = self.__listSensorSectionsOfPath(path, direction)  # sensor sections of path

    """ TODO: Refine code
        記錄路徑中所有的測站區間
    """
    def __listSectionsOfPath(self, path, direction):
        sections = []
        flag = False
        start, end = (path[0], path[1]) if direction == '南' \
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

    def __filterDataByDirection(self, direction):
        def myFilter(pred, xs):
            return [e for e in xs if pred(e, dire)]

        direction = 'S' if direction == "南" else 'N'
        predicate = lambda e: e[3] == direction
        return (e for e in self.__data if predicate(e))

    def __readData(self, step2_output_dir):
        def fn(row):
            return [row[0],
                    InterchangeSection(start=row[1], dest=row[2]),
                    row[3], row[4:]]
        def fn2(row):
            return [InterchangeSection(start=row[0], dest=row[1]), row[2]]

        data = CSVUtil.read(step2_output_dir)
        self.__data_header = data[0]
        self.__data = [fn(row) for row in data[1:]]
        Path.targets = [ fn2(row) for row in MYPATHS ]

# End of Path

if __name__ == "__main__":
    step3 = Path()
    step3.test()
