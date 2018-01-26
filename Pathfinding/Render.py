# -*- coding: utf8 -*-

"""Render.py

Render.py can render .map files, along with any pathing information.
"""

#
# Built-in imports.
#

import json
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

def Render(MapData, FileName = None, PathInformation = None):
    # Create blank image.
    Image = np.zeros((MapData["Size"][1] + RenderBorder * 2, MapData["Size"][0] + RenderBorder * 2, 3), np.uint8)
    # Round every coordinate value.
    for Element in MapData["Elements"]:
        for Index, Point in enumerate(MapData["Elements"][Element]["Points"]):
            MapData["Elements"][Element]["Points"][Index][1] = abs(MapData["Elements"][Element]["Points"][Index][1] - MapData["Size"][1]) # Invert Y values, because OpenCV starts Y axis from the top-down
            MapData["Elements"][Element]["Points"][Index] = [round(Item + RenderBorder) for Item in Point]
        if "InteractiveFaces" in MapData["Elements"][Element]:
            for FaceIndex, Face in enumerate(MapData["Elements"][Element]["InteractiveFaces"]):
                for PointIndex, Point in enumerate(MapData["Elements"][Element]["InteractiveFaces"][FaceIndex]):
                    MapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex][1] = abs(MapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex][1] - MapData["Size"][1]) # Invert Y values, because OpenCV starts Y axis from the top-down
                    MapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex] = [round(Item + RenderBorder) for Item in Point]
    # Draw.
    for Element in MapData["Elements"]:
        if MapData["Elements"][Element]["Solidity"] == 0: # Completely transversable; not solid.
            cv2.polylines(Image, np.array([MapData["Elements"][Element]["Points"]]), True, (255, 0, 0))
        elif MapData["Elements"][Element]["Solidity"] == 1: # Solid. Map element.
            cv2.polylines(Image, np.array([MapData["Elements"][Element]["Points"]]), True, (88, 88, 88))
        elif MapData["Elements"][Element]["Solidity"] == 2: # Solid. Anomalous element.
            cv2.polylines(Image, np.array([MapData["Elements"][Element]["Points"]]), True, (0, 0, 255))
        if "InteractiveFaces" in MapData["Elements"][Element]:
            for FaceIndex, Face in enumerate(MapData["Elements"][Element]["InteractiveFaces"]):
                cv2.line(Image, tuple(Face[0]), tuple(Face[1]), (0, 128, 0), 1)
        if PathInformation:
            pass
    # Save.
    if FileName:
        NewFileName = "{0}.png".format(FileName)
    else:
        NewFileName = "Render {0}.png".format(time.strftime("%Y-%m-%d %H:%M:%S"))
    Log("Saving render \"{0}\".".format(NewFileName), 0)
    cv2.imwrite("{0}/{1}".format(Config["RenderStorageLocation"], NewFileName), Image)

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
