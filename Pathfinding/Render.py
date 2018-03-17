# -*- coding: utf8 -*-

"""Render.py

Render.py can render .map files, along with any pathing information.
"""

#
# Built-in imports.
#

from copy import deepcopy
import json
import math
import sys
import time

#
# Custom imports.
#

import cv2
import numpy as np

import Configuration
from Log import Log

#
# Global variables.
#

Config = Configuration.LoadConfig()
RenderBorder = Config["RenderImageBorder"]
 
#
# Functions.
#

def Render(MapData, FileName = None, PathInformation = None): # TODO: Simplify FOR statements.
    """
    Saves an image with colored lines representing any passed MapData and PathInformation.
    """
    RenderMapData = deepcopy(MapData) # Make a copy of MapData so that we don't modify the original variable's value.
    # Create blank image.
    Image = np.zeros((RenderMapData["Size"][1] + RenderBorder * 2, RenderMapData["Size"][0] + RenderBorder * 2, 3), np.uint8)
    # Round every coordinate value, add RenderBorder, and invert Y axis.
    for Element in RenderMapData["Elements"]:
        for Index, Point in enumerate(RenderMapData["Elements"][Element]["Points"]):
            RenderMapData["Elements"][Element]["Points"][Index][1] = abs(RenderMapData["Elements"][Element]["Points"][Index][1] - RenderMapData["Size"][1]) # Invert Y values, because OpenCV starts Y axis from the top-down
            RenderMapData["Elements"][Element]["Points"][Index] = [round(Item + RenderBorder) for Item in Point]
        if "InteractiveFaces" in RenderMapData["Elements"][Element]:
            for FaceIndex, Face in enumerate(RenderMapData["Elements"][Element]["InteractiveFaces"]):
                for PointIndex, Point in enumerate(RenderMapData["Elements"][Element]["InteractiveFaces"][FaceIndex]):
                    RenderMapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex][1] = abs(RenderMapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex][1] - RenderMapData["Size"][1]) # Invert Y values, because OpenCV starts Y axis from the top-down
                    RenderMapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex] = [round(Item + RenderBorder) for Item in Point]
    if PathInformation:
        for ItemIndex, Item in enumerate(PathInformation):
            if type(Item) != str:
                for CoordinateIndex, Coordinate in enumerate(Item):
                    Coordinate[1] = abs(Coordinate[1] - RenderMapData["Size"][1])
                    PathInformation[ItemIndex][CoordinateIndex] = [round(Item + RenderBorder) for Item in Coordinate]
    # Draw.
    for Element in RenderMapData["Elements"]:
        if RenderMapData["Elements"][Element]["Solidity"] == 0: # Completely transversable; not solid.
            cv2.polylines(Image, np.array([RenderMapData["Elements"][Element]["Points"]]), True, (255, 0, 0))
        elif RenderMapData["Elements"][Element]["Solidity"] == 1: # Solid. Map element.
            cv2.polylines(Image, np.array([RenderMapData["Elements"][Element]["Points"]]), True, (88, 88, 88))
        elif RenderMapData["Elements"][Element]["Solidity"] == 2: # Solid. Anomalous element.
            cv2.polylines(Image, np.array([RenderMapData["Elements"][Element]["Points"]]), True, (0, 0, 255))
        elif RenderMapData["Elements"][Element]["Solidity"] == 3: # Solid. Virtual "expanded" element.
            cv2.polylines(Image, np.array([RenderMapData["Elements"][Element]["Points"]]), True, (255, 255, 255))
        if "InteractiveFaces" in RenderMapData["Elements"][Element]:
            for FaceIndex, Face in enumerate(RenderMapData["Elements"][Element]["InteractiveFaces"]):
                cv2.line(Image, tuple(Face[0]), tuple(Face[1]), (0, 128, 0), 1)
    if PathInformation:
        for Item in PathInformation:
            if type(Item) != str:
                cv2.polylines(Image, np.array([Item]), False, (0, 255, 0))
                for Coordinate in Item:
                    cv2.circle(Image, tuple(Coordinate), 2, (0, 200, 0), -1)
    # Save.
    if FileName:
        NewFileName = "{0}.png".format(FileName)
    else:
        NewFileName = "Render {0}.png".format(time.strftime("%Y-%m-%d %H%M%S"))
    Log("Saving render \"{0}\".".format(NewFileName), 0)
    cv2.imwrite("{0}/{1}".format(Config["RenderStorageLocation"], NewFileName), Image)

def RenderPoints(MapData, Points):
    """
    Render some points.
    """
    RenderMapData = deepcopy(MapData) # Make a copy of MapData so that we don't modify the original variable's value.
    Image = np.zeros((RenderMapData["Size"][1] + RenderBorder * 2, RenderMapData["Size"][0] + RenderBorder * 2, 3), np.uint8)
    for Point in Points:
        X, Y = int(round(Point[0])), int(round(Point[1]))
        NewY = abs(Y - len(RenderMapData)) + RenderBorder
        NewX = X + RenderBorder
        cv2.rectangle(Image, (NewX, NewY), (NewX, NewY), (255, 255, 255), -1)
    cv2.imwrite("{0}/{1}".format(Config["RenderStorageLocation"], "ExpectedLidarRender.png"), Image)

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
