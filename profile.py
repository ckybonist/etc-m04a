#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def timing(f, n, a):
    print (f.__name__)
    r = range(n)
    t1 = time.clock()
    for i in r:
        f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a)
    t2 = time.clock()
    print(round(t2-t1, 3))

def timing2(f, n):
    print(f.__name__)
    r = range(n)
    t1 = time.clock()
    for i in r:
        f(); f(); f(); f(); f(); f(); f(); f(); f(); f()
    t2 = time.clock()
    print(round(t2-t1, 3))

def timing3(f, n, a, b):
    print(f.__name__)
    r = range(n)
    t1 = time.clock()
    for i in r:
        f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b);
    t2 = time.clock()
    print(round(t2-t1, 3))
