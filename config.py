#!/usr/bin/env python3
# -*- coding: utf-8 -*-


FILE_EXT = ".csv"
INPUT_DIR = "data"
OUTPUT_DIR = "output"

NUM_CAR_TYPE = 5
TIME_INTERVAL = 5   # minutes
DEFAULT_SPEED = 80  # km/h

MYPATHS = [
    ("圓山", "高雄(九如路)", "S"),
    ("圓山", "台中", "S"),
    ("台中", "高雄(九如路)", "S"),
    ("圓山", "林口(文化一路)", "S"),
    ("圓山", "新竹系統", "S"),
    ("高雄(九如路)", "圓山", "N"),
    ("台中", "圓山", "N"),
    ("高雄(九如路)", "台中", "N"),
    ("林口(文化一路)", "圓山", "N"),
    ("新竹系統", "圓山", "N"),
    ("南港", "九如", "S"),
    ("南港", "沙鹿", "S"),
    ("沙鹿", "九如", "S"),
    ("南港", "鶯歌系統", "S"),
    ("九如", "南港", "N"),
    ("沙鹿", "南港", "N"),
    ("九如", "沙鹿", "N"),
    ("鶯歌系統", "南港", "N"),
    ("南港系統", "蘇澳", "S"),
    ("蘇澳", "南港系統", "N"),
]

IGNORE_SENSORS = [
    "05FR143N",
    "05FR113S",
    "01F3252S",
    "03F0498S",
    "03F2447S",
    "03F2447N",
]
