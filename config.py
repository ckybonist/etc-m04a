#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple


DATA_EXT = '.csv'
NUM_CAR_TYPE = 5
TIME_INTERVAL = 5  # minutes
INPUT_DIR = 'data/'
OUTPUT_DIR = 'output/'
SensorSection = namedtuple("SensorSection", ["entry", "exit"])  # where the magic happens
