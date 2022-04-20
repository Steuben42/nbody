# -*- coding: utf-8 -*-
"""
nbody.utilities.logging
"""

import csv 
import logging

### LOGGIN MODULE SETUP ###
logging.basicConfig(filename='messages.log', encoding='utf-8', format='%(levelname)s:%(module)s:%(funcName)s [%(asctime)s] %(message)s', level=logging.DEBUG)


### FILES ###
def initFiles(dir):
    with open(dir + 'dataLog.csv', 'w', newline='') as file:
        w = csv.writer(file)
        w.writerow([None])

    return