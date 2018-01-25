"""Pathfinding.py

Pathfinding.py calculates the shortest path for the robot between it's current location and any number of locations.
"""

#
# Built-in imports.
#

import math
from operator import itemgetter

#
# Custom imports.
#

import Configuration
from Log import Log

#
# Global variables.
#

Config = Configuration.LoadConfig()

#
# Functions.
#

def FindNearestActionableElementFace():
    pass

def GetIntersectionPoint(LineOne, LineTwo): # Returns False if line segments do not intersect. Credit for this function goes to Paul Draper. See https://stackoverflow.com/a/20677983 for source.
    XDifference = (LineOne[0][0] - LineOne[1][0], LineTwo[0][0] - LineTwo[1][0])
    YDifference = (LineOne[0][1] - LineOne[1][1], LineTwo[0][1] - LineTwo[1][1])
    def Det(A, B):
        return A[0] * B[1] - A[1] * B[0]
    Div = Det(XDifference, YDifference)
    if Div == 0:
        return False
    D = (Det(*LineOne), Det(*LineTwo))
    X = Det(D, XDifference) / Div
    Y = Det(D, YDifference) / Div
    return (X, Y)

def GetQuadrants(Angle):
        StepQuadrants = []
        if Angle == 0:
            StepQuadrants = (1, 4)
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

def ParseInstructions(Instructions):
    Log("Parsing pathing instructions.", 0)
    SplitInstructions = Instructions.split(",")
    ParsedInstructions = {"CurrentPosition": (int(SplitInstructions[0]), int(SplitInstructions[1])), "CurrentRotation": int(SplitInstructions[2]), "ElementDistribution": SplitInstructions[3], "PathList": SplitInstructions[4:]}
    return ParsedInstructions

def Path(MapData, CurrentPosition, ElementDistribution, PathList):
    Log("Pathing instructions:\r\n                                 - Initial position: {0}\r\n                                 - Element distribution: {1}\r\n                                 - Path list: {2}".format(CurrentPosition, ElementDistribution, PathList), 0)
    PathInformation = []
    TargetPoints = []
    for Item in PathList:
        if Item.lower() in ("deliver", "collect"): # If the item is an action.
            PathInformation.append(Item)
        elif len(Item) == 2: # If the item is a location (pair of coordinates).
            TargetPoints.append(Item)
        else: # If the item is a pre-defined location, as described in the .map file.
            if not Item in MapData["Elements"]:
                Log("Path target \"{0}\" is not described in map file.".format(Element), 3)
                return
            if "InteractiveFaces" in MapData["Elements"][Item]:
                FacesToEvaluate = []
                if "InteractiveSides" in MapData["Elements"][Item]:
                    if Item == "NearSwitch":
                        if ElementDistribution[0] == "L":
                            for Index in MapData["Elements"][Item]["InteractiveSides"]["Left"]:
                                FacesToEvaluate.append(MapData["Elements"][Item]["InteractiveFaces"][Index])
                        else:
                            for Index in MapData["Elements"][Item]["InteractiveSides"]["Right"]:
                                FacesToEvaluate.append(MapData["Elements"][Item]["InteractiveFaces"][Index])
                    elif Item == "Scale":
                        if ElementDistribution[0] == "L":
                            for Index in MapData["Elements"][Item]["InteractiveSides"]["Left"]:
                                FacesToEvaluate.append(MapData["Elements"][Item]["InteractiveFaces"][Index])
                        else:
                            for Index in MapData["Elements"][Item]["InteractiveSides"]["Right"]:
                                FacesToEvaluate.append(MapData["Elements"][Item]["InteractiveFaces"][Index])
                    elif Item == "FarSwitch":
                        if ElementDistribution[0] == "L":
                            for Index in MapData["Elements"][Item]["InteractiveSides"]["Left"]:
                                FacesToEvaluate.append(MapData["Elements"][Item]["InteractiveFaces"][Index])
                        else:
                            for Index in MapData["Elements"][Item]["InteractiveSides"]["Right"]:
                                FacesToEvaluate.append(MapData["Elements"][Item]["InteractiveFaces"][Index])
                else:
                    FacesToEvaluate = MapData["Elements"]["Item"]
                FaceCenters = []
                FaceDistances = []
                for Face in FacesToEvaluate: # Determine the nearest face.
                    FaceCenter = (Face[0][0] + Face[1][0]) / 2, (Face[0][1]) / 2
                    FaceCenters.append(FaceCenter)
                    Distance = abs(FaceCenter[0] - CurrentPosition[0]) + abs(FaceCenter[1] - CurrentPosition[1])
                    FaceDistances.append(Distance)
                TargetPoints.append(FaceCenters[min(enumerate(FaceDistances), key=itemgetter(1))[0]])
            else:
                Log("Path target \"{0}\" does not have any InteractiveFaces.", 2)
                # Put down a point to path to regardless. (Use the center of the element.)
                X, Y = zip(MapData["Elements"][Item]["Points"])
                Length = len(X)
                TargetPoints.append((sum(X) / L, sum(Y) / L))
    LinesEvaluated = 0
    StartPoint = []
    EndPoint = []
    PathPoints = []
    while LinesEvaluated < len(TargetPoints): # Evaluate the shortest path between the current location and each of the points listed.
        if LinesEvaluated == 0:
            StartPoint = CurrentPosition
            EndPoint = TargetPoints[0]
        else:
            StartPoint = TargetPoints[LinesEvaluated - 1]
            EndPoint = TargetPoints[LinesEvaluated]
        # Check for intersections, and path around them.
        # Filter out possible intersections with elements by only searching for ones which exist within the quadrant of the vector's direction.
        Angle = round(math.degrees(math.atan2(EndPoint[1] - StartPoint[1], EndPoint[0] - StartPoint[0])))
        if Angle < 0:
            Angle = 360 + Angle
        StepQuadrants = GetQuadrants(Angle)
        if len(StepQuadrants) > 1:
            Plural = "s"
        else:
            Plural = ""
        Log("Pathfinding started for step {0}. Step starts at point \"{1}\" and ends at point \"{2}\", and has an angle of {3}°, therefore extending into quadrant{4} {5}.".format(LinesEvaluated + 1, StartPoint, EndPoint, Angle, Plural, StepQuadrants), 0)
        ElementsToEvaluate = []
        for Element in MapData["Elements"]:
            if any(GetQuadrants(round(math.degrees(math.atan2(Point[1] - StartPoint[1], Point[0] - StartPoint[0])))) == StepQuadrants for Point in MapData["Elements"][Element]["Points"]): # If any of the element's points exist within the proper quadrant(s).
                ElementsToEvaluate.append(Element)
        Log("Pathfinding is evaluating potential element intersections for path step {0}.".format(LinesEvaluated + 1), 0)
        for Element in ElementsToEvaluate:
            Log("Pathfinding is evaluating intersections with element \"{0}\".".format(Element), 0)
            # TODO: Evaluate intersections and path around elements as needed. Append new points to PathPoints.
        PathPoints.append(TargetPoints) # TODO: Update this.
        Log("Pathfinding completed for step {0} of {1}".format(LinesEvaluated + 1, len(TargetPoints)), 0)
        LinesEvaluated += 1
    PathInformation.append(PathPoints) # TODO: Update this.
    Log("Pathfinding complete.", 0)
    # Return a list of points that make up the path, along with actions to be taken. Formatted as a tuple:
    # [(X, Y), (X, Y), "DELIVER", (X, Y), "COLLECT", (X, Y), (X, Y), "DELIVER"]
    print(str(PathInformation)) # TODO TEMP
    return PathInformation

def VectorizePathInformation(PathInformation):
    pass

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")