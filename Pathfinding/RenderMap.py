"""RenderMap.py renders the game map file.

Please note that this script was not programmed with "quality coding" in mind - this issue will be fixed shortly.
"""

import json
import sys
import time

import numpy as np
import cv2

# SETTINGS

Version = "1.0"
RenderBorder = 20

# START CODE

MapData = []
print("RenderMap Version " + Version + ".")
# MapPath = input("Enter the path of the .map file you would like to render:\r\n > ")
MapPath = "FRC_Field_2018.map"
print("Reading map file...")
try:
    with open(MapPath, "r") as File:
        MapData = json.load(File)
except FileNotFoundError:
    print("Unable to read map file: File does not exist.")
    sys.exit()
except PermissionError:
    print("Unable to read map file: Insufficient permissions.")
    sys.exit()
#except:
    #print("Unable to read map file.")
    #sys.exit()

print("Rendering map...")
print("Image dimensions: " + str(MapData["Size"][0] + RenderBorder * 2) + ", " + str(MapData["Size"][1] + RenderBorder * 2) + ".")

Image = np.zeros((MapData["Size"][1] + RenderBorder * 2, MapData["Size"][0] + RenderBorder * 2, 3), np.uint8)

# Make every number nice and round.
for Element in MapData["Elements"]:
    print("Rendering Element: " + str(Element))
    for Index, Point in enumerate(MapData["Elements"][Element]["Points"]):
        MapData["Elements"][Element]["Points"][Index] = [round(Item + RenderBorder) for Item in Point]
    if "InteractiveFaces" in MapData["Elements"][Element]:
        for FaceIndex, Face in enumerate(MapData["Elements"][Element]["InteractiveFaces"]):
            for PointIndex, Point in enumerate(MapData["Elements"][Element]["InteractiveFaces"][FaceIndex]):
                MapData["Elements"][Element]["InteractiveFaces"][FaceIndex][PointIndex] = [round(Item + RenderBorder) for Item in Point]


# Draw
for Element in MapData["Elements"]:
    if MapData["Elements"][Element]["Solidity"] == 0:
        cv2.polylines(Image, np.array([MapData["Elements"][Element]["Points"]]), True, (255, 0, 0))
    elif MapData["Elements"][Element]["Solidity"] == 1:
        Points = np.array(MapData["Elements"][Element]["Points"])
        cv2.fillPoly(Image, [Points], (88, 88, 88))
    if "InteractiveFaces" in MapData["Elements"][Element]:
        for FaceIndex, Face in enumerate(MapData["Elements"][Element]["InteractiveFaces"]):
            cv2.line(Image, tuple(Face[0]), tuple(Face[1]), (0, 255, 0), 1)
            

print("Map render complete.")

cv2.imshow("Map Render", Image)
cv2.waitKey(0)