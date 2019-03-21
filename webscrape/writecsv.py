#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 00:24:31 2019

@author: bin
"""

import csv

with open('profrating.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    [writer.writerows([i]) for i in All]
csvFile.close()

