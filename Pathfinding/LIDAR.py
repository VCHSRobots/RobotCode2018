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

def Compare():
    pass

def CompressCurrentData(Data):
    pass

def GetCurrentData():
    FOV = Config["LIDARFOV"]
    CurrentPosition = None
    CurrentRotation = None
    AnomalousElements = None
    # TODO: Get latest LIDAR sweep data, parse. Get position data, rotation data, and any anomalous elements using the dot products of two lists (MapData and lidar measurements). 
    return CurrentPosition, CurrentRotation, AnomalousElements

def GetExpectedData():
    return ExpectedPosition, ExpectedRotation # We already know the expected map elements via MapData["Elements"].

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
