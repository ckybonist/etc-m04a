#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from sensors import step1
import step2
from path import PATHS



"""
    Predict travel times of paths. The whole process can be splitted
    into three steps.
"""
def predict():
    #step1()
    process2 = step2.Analyzer()
    result = process2.run(PATHS)
    print(len(result))
    print(result[3][1])
    #step3()


if __name__ == "__main__":
    predict()
