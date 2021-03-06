# -*- coding: utf8 -*-

"""LIDAR.py

LIDAR.py compares measurements between expected and actual LIDAR sweeps at a specific point, and returns the coordinate offset.
"""

#
# Built-in imports.
#

import json
import math
from operator import itemgetter
import sys
import time

#
# Custom imports.
#

import numpy as np
import serial

import Configuration
from Log import Log
from Render import RenderPoints

#
# Global variables.
#

Config = Configuration.LoadConfig()

with open(Config["MapSource"]) as File:
    LIDARMapData = json.load(File)

SolidElements = [] # We only need to calculate this once...
for MapElement in LIDARMapData["Elements"]:
    if LIDARMapData["Elements"][MapElement]["Solidity"] >= 1:
        SolidElements.append(MapElement)

#
# Functions.
#

def Compare(CurrentData, ExpectedData):
    """
    Determines the difference between CurrentData and ExpectedData in degrees and X, Y.
    """
    # TODO: Calculate difference in angle, (X, Y). Use Dot-Product multiplication? Also detect, expand, and return any AnomalousElements.
    pass

def GetCurrentData():
    """
    Collects, calculates, and returns the current position data from the latest LIDAR sweep.
    """
    FOV = Config["LIDARFOV"] # FOV is a range between two angles - for example, from 0 to 180 degrees.
    CurrentPosition = None
    CurrentRotation = None
    AnomalousElements = None
    CurrentData = CurrentPosition, CurrentRotation, AnomalousElements
    # TODO: Get latest LIDAR sweep data, parse.
    return CurrentData

def GetExpectedData(CurrentPosition, CurrentRotation):
    """
    Estimates and returns the expected LIDAR values based on the current expected location.
    """
    FOV = Config["LIDARFOV"] # A bound of two angles, relative to the robot's personal orientation. ALWAYS centered around 0 degrees. First is a negative degree (moving clockwise), second is positive (moving counterclockwise).
    ScanRate = Config["LIDARSampleRate"] / Config["LIDARRotationRate"] # Measurments-Per-Rotation
    SweepSize = abs(FOV[0] - FOV[1])
    IncrementSize = 360 / ScanRate # We get a data point every "IncrementSize" degrees, bound by the angles described by "FOV".
    NumberOfVectors = math.floor(SweepSize / IncrementSize)
    VectorsAnalyzed = 0
    ExpectedData = []
    while VectorsAnalyzed < NumberOfVectors:
        Angle = VectorsAnalyzed * IncrementSize + CurrentRotation
        if Angle > 359:
            Angle = abs(360 - Angle) # No angles larger than 255!
        Intersection = Scan(CurrentPosition, Angle)
        TempFile = open("TestPostulation.csv", "a")
        TempFile.write("{0}, {1}\r\n".format(Intersection[0], Intersection[1]))
        ExpectedData.append(Intersection)
        VectorsAnalyzed += 1
        print("VectorsAnalyzed: {0} / {1}".format(VectorsAnalyzed, NumberOfVectors)) # TODO: TEMP
    RenderPoints(LIDARMapData, ExpectedData)
    return ExpectedData

def GetIntersectionPoint(VectorOrigin, VectorAngle, Line,): # Finds intersection between a vector and a line segment.
    """
    Finds the intersection point between a vector and a line segment.
    """
    X, Y = VectorOrigin
    (X1, Y1), (X2, Y2) = Line
    DX = math.cos(VectorAngle)
    DY = math.sin(VectorAngle)
    if DX == 0 or X2 - X1 == 0: # No dividing by zero! This means that we don't have an intersection.
        return None
    if DY / DX != (Y2 - Y1) / (X2 - X1):
        D = (DX * (Y2 - Y1)) - DY * (X2 - X1)
        if D != 0:
            R = (((Y - Y1) * (X2 - X1)) - (X - X1) * (Y2 - Y1)) / D
            S = (((Y - Y1) * DX) - (X - X1) * DY) / D
            if R >= 0 and 0 <= S <= 1:
                IntersectionPoint = (X + R * DX, Y + R * DY)
                return IntersectionPoint
    return None # Returning None because they do not intersect.

def InitializeLIDAR():
    Log("Initializing LIDAR device.", 0)
    SweepLocation = Config["LIDARLocation"]
    try:
        Sweep = serial.Serial(SweepLocation, baudrate=115200, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False, rtscts=False, dsrdtr=False)
    except:
        Log("Unable to detect LIDAR device. Check \"LIDARLocation\" in configuration file.", 3)
        return
    SweepReady = False
    while not SweepReady:
        Sweep.write(b"MZ\n") # Check if motor is ready.
        MotorStatus = Sweep.readline().decode("utf-8")[2:4]
        if MotorStatus == "01":
            time.sleep(1)
        else:
            SweepReady = True
    Sweep.write(b"IV\n")
    SweepInformation = Sweep.readline().decode("utf-8")[2:-1]
    # Log("LIDAR device information:\r\n                                - Model: {0}\r\n                                - Protocol: {1}\r\n                                - Firmware version: {2}\r\n                                - Hardware version: {3}\r\n                                - Serial number: {4}".format(SweepInformation[0:5], SweepInformation[6:7], SweepInformation[8:9], SweepInformation[10], SweepInformation[11:19]), 0)
    Sweep.write(b"MI\n")
    MotorSpeed = Sweep.readline().decode("utf-8")[2:4]
    DesiredMotorSpeed = str(Config["LIDARRotationRate"]).zfill(2)
    if MotorSpeed != DesiredMotorSpeed:
        Log("Current LIDAR rotation rate is {0} Hz. Adjusting to desired rate of {1} Hz.".format(MotorSpeed, DesiredMotorSpeed), 0)
        Sweep.write("MS{0}\n".format(DesiredMotorSpeed).encode())
        Response = Sweep.readline().decode("utf-8") # Just reading the line so we clear that variable for the next time we want to write / read.
        SweepReady = False
        while not SweepReady:
            Sweep.write(b"MZ\n") # Check if motor is ready.
            MotorStatus = Sweep.readline().decode("utf-8")[2:4]
            if MotorStatus == "01":
                time.sleep(1)
            else:
                SweepReady = True
    Sweep.write(b"LI\n")
    SampleRate = Sweep.readline().decode("utf-8")[2:4]
    DesiredSampleRate = Config["LIDARSampleRate"]
    if SampleRate == "01":
        SampleRate = 500
    elif SampleRate == "02":
        SampleRate = 750
    elif SampleRate == "03":
        SampleRate = 1000
    if SampleRate != DesiredSampleRate:
        Log("Current LIDAR sample rate is {0} Hz. Adjusting to desired rate of {1} Hz.".format(SampleRate, DesiredSampleRate), 0)
        if DesiredSampleRate == 500:
            Rate = "01"
        elif DesiredSampleRate == 750:
            Rate = "02"
        elif DesiredSampleRate == 1000:
            Rate = "03"
        else:
            Log("Invalid LIDARSampleRate described in configuration.", 3)
            Rate = "03"
        Sweep.write("LR{0}\n".format(Rate).encode())
    Log("Current LIDAR rotation rate: {0} Hz. Current LIDAR sample rate: {1} Hz.".format(DesiredMotorSpeed, DesiredSampleRate), 1)

def Scan(OriginPoint, VectorAngle):
    """
    Returns the distance and (X, Y) coordinate for the first point encountered along the vector.
    """
    def GetQuadrants(Angle):
        StepQuadrants = []
        if Angle == 0:
            StepQuadrants = [1, 4]
        elif 0 < Angle < 90:
            StepQuadrants = [1]
        elif Angle == 90:
            StepQuadrants = [1, 2]
        elif 90 < Angle < 180:
            StepQuadrants = [2]
        elif Angle == 180:
            StepQuadrants = [2, 3]
        elif 180 < Angle < 270:
            StepQuadrants = [3]
        elif Angle == 270:
            StepQuadrants = [3, 4]
        elif 270 < Angle < 360:
            StepQuadrants = [4]
        return StepQuadrants

    ElementIntersections = []
    for Element in SolidElements:
        ElementLinesEvaluated = 0
        while ElementLinesEvaluated < len(LIDARMapData["Elements"][Element]["Points"]) - 1:
            Line = (LIDARMapData["Elements"][Element]["Points"][ElementLinesEvaluated], LIDARMapData["Elements"][Element]["Points"][ElementLinesEvaluated + 1])
            IntersectionPoint = GetIntersectionPoint(OriginPoint, VectorAngle, Line)
            if IntersectionPoint:
                Distance = math.hypot(IntersectionPoint[0] - OriginPoint[0], IntersectionPoint[1] - OriginPoint[1])
                ElementIntersections.append((Element, IntersectionPoint, Distance))
            ElementLinesEvaluated += 1
    if ElementIntersections:
        ClosestElementIntersection = sorted(ElementIntersections, key=itemgetter(2))[0]
        return ClosestElementIntersection[1]
        print("ClosestElementIntersection = {0}".format(ClosestElementIntersection)) # TODO: TEMP
    else:
        return OriginPoint # We return nothing because there was no intersection.
        print("ClosestElementIntersection = {0}".format("NaN")) # TODO: TEMP

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
