# -*- coding: utf8 -*-

"""LIDAR.py

LIDAR.py compares measurements between expected and actual LIDAR sweeps at a specific point, and returns the coordinate offset.
"""

#
# Custom imports.
#

import Configuration
from Pathfinding import GetIntersectionPoint

#
# Global variables.
#

Config = Configuration.LoadConfig()

#
# Functions.
#

def Compare(CurrentData, ExpectedData):
    if len(CurrentData) > len(ExpectedData):
        ExpectedData = ExpandExpectedData(ExpectedData) # Expand ExpectedData to the size of the observed CurrentData. This preserves the higher data density of CurrentData, which will be usefull if any AnomalousElements are detected.
    elif len(CurrentData) < len(ExpectedData):
        ExpectedData = CompressCurrentData(ExpectedData) # Compress ExpectedData to the size of the observed CurrentData. This at least preserves the original data density of CurrentData.
    # TODO: Calculate difference in angle, (X, Y). Use Dot-Product multiplication? Also detect any AnomalousElements.
    pass

def CompressExpectedData(ExpectedData):
    # TODO: Compress.
    return ExpectedData

def ExpandExpectedData(ExpectedData):
    # TODO: Expand.
    return ExpectedData

def GetCurrentData():
    FOV = Config["LIDARFOV"]
    CurrentPosition = None
    CurrentRotation = None
    AnomalousElements = None
    CurrentData = CurrentPosition, CurrentRotation, AnomalousElements
    # TODO: Get latest LIDAR sweep data, parse.
    return CurrentData

def GetExpectedData(CurrentPosition, CurrentRotation):
    FOV = Config["LIDARFOV"]
    ExpectedData = None
    return ExpectedData

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
