#!/usr/bin/env python
# -*- coding: utf-8 -*-

from path import PATHS
from utils import CSVUtil


SENSOR_LOCATIONS = CSVUtil.read("resource/etc-sensor-loc.csv")


def calc_interchange_travel_time(path):
    pass



if __name__ == "__main__":
    path = ("圓山", "三重", "南", "05")
    ACTUAL_TIME = 196.2

    csv = CSVUtil()
    data = csv.read("resource/sensor_section.example.csv")
    result = calc_interchange_travel_time(path)




