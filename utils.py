#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

class CSVUtil:
    def __init__(self):
        pass
# fname: file name
# deli: delimiter (default to excel)
# dialect: excel or excel-tab (default to comma)
    def read(self, fname, dia = 'excel', deli = ','):
        with open(fname, 'r') as f:
            reader = csv.reader(f, dialect = dia, delimiter = deli)
            return [ tuple(r) for r in reader ]

# data: list or something...
# others same as above
    def write(self, data, fname, dia = 'excel' , deli = ','):
        with open(fname, 'w') as f:
            writer = csv.writer(f, dialect = dia, delimiter = deli)
            for r in data:
                writer.writerow(r)
