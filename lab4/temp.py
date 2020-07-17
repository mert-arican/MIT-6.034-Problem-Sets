#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:23:38 2020

@author: mertarican
"""

a = dict()

li = ["S", "R", "S", "S", "S", "R", "R", "I", "I", "S"]

for decision in li:
    if decision in a:
        a[decision] += 1
    else:
        a[decision] = 1

#print(len(decision))
