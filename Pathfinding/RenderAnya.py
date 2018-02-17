# -*- coding: utf8 -*-

import time

import cv2
import numpy as np

import Configuration
from Log import Log

Config = Configuration.LoadConfig()
RenderBorder = Config["RenderImageBorder"]

#
# Temporary file. Contents of function RenderAnya will be placed into Render.py upon completion.
#

def RenderAnya(GridData, FileName = None, PathInformation = None):
    GridHeight = len(GridData) - 1 # We subtract one because lists start at zero. If we want to reference the right-most coordinate, we would otherwise run into an error (address an index that is one-out-of-bounds).
    GridWidth = len(GridData[0]) - 1
    Image = np.zeros((GridHeight + RenderBorder * 2, GridWidth + RenderBorder * 2, 3), np.uint8)
    for LineIndex, Line in enumerate(GridData):
        for PointIndex, Point in enumerate(Line):
            if GridData[LineIndex][PointIndex] == 1:
                # We need to invert the Y axis...
                NewLineIndex = abs(LineIndex - GridHeight) + RenderBorder
                NewPointIndex = PointIndex + RenderBorder
                cv2.rectangle(Image, (NewPointIndex, NewLineIndex), (NewPointIndex, NewLineIndex), (255, 255, 255), -1)
    if PathInformation:
        pass # TODO: Render PathInformation
    NewFileName = "AnyaRender {0}.png".format(time.strftime("%Y-%m-%d %H%M%S"))
    Log("Saving render \"{0}\".".format(NewFileName), 0)
    cv2.imwrite("{0}/{1}".format(Config["RenderStorageLocation"], NewFileName), Image)