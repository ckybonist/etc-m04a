#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from sensor import Sensor as Step1
from interchange import Interchange as Step2
from path import Path as Step3


def run():
    """
        Estimate travel times of each path. The whole process comprieses
        three steps.
    """
    step1 = Step1()
    step1.analyze()

    step2 = Step2()
    step2.analyze()

    step3 = Step3()
    step3.analyze()


if __name__ == "__main__":
    t1 = time.clock()
    run()
    t2 = time.clock()
    print("Time: {}".format(round(t2-t1, 3)))
