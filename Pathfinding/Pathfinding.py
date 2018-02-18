# -*- coding: utf8 -*-

"""Pathfinding.py

Pathfinding.py calculates the shortest path for the robot between it's current location and any number of locations.
"""

#
# Built-in imports.
#

from collections import namedtuple
from copy import deepcopy
import math
from operator import itemgetter

#
# Custom imports.
#

from Anya import Anya
import Configuration
from Log import Log

#
# Global variables.
#

Config = Configuration.LoadConfig()

#
# Functions.
#

def BresenhamLinePoints(StartPoint, EndPoint):
    """
    Returns every point that lies along the line created by the StartPoint and the EndPoint.
    Algorithm based on the example at http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python.
    """
    X1, Y1 = [int(round(Number)) for Number in StartPoint]
    X2, Y2 = [int(round(Number)) for Number in EndPoint]
    DX = X2 - X1
    DY = Y2 - Y1
    IsSteep = abs(DY) > abs(DX)
    if IsSteep:
        X1, Y1 = Y1, X1
        X2, Y2 = Y2, X2
    Swapped = False
    if X1 > X2:
        X1, X2 = X2, X1
        Y1, Y2 = Y2, Y1
        Swapped = True
    DX = X2 - X1
    DY = Y2 - Y1
    Error = int(DX / 2.0)
    YStep = 1 if Y1 < Y2 else -1
    Y = Y1
    Points = []
    for X in range(X1, X2 + 1):
        Coordinate = (Y, X) if IsSteep else (X, Y)
        Points.append(Coordinate)
        Error -= abs(DY)
        if Error < 0:
            Y += YStep
            Error += DX
    if Swapped:
        Points.reverse()
    return Points

def ExpandMapElements(MapData):
    """
    Creates a large "virtual element" around specified solid map elements, and appends it to the MapData["Elements"] list. Returns the modified MapData.
    """
    CopiedMapData = deepcopy(MapData)
    RobotRadius = max(Config["RobotDimensions"]) / 2
    VirtualElements = {}
    for Element in CopiedMapData["Elements"]:
        if Element not in Config["NonVirtualizableElements"]:
            if CopiedMapData["Elements"][Element]["Solidity"] >= 1:
                VirtualElement = {"Points": [], "Solidity": 3}
                X, Y = zip(*CopiedMapData["Elements"][Element]["Points"])
                Length = len(X)
                ElementCenter = (sum(X) / Length, sum(Y) / Length)
                for Point in CopiedMapData["Elements"][Element]["Points"]:
                    RelativePoint = [0, 0]
                    RelativePoint[0] = Point[0] - ElementCenter[0]
                    RelativePoint[1] = Point[1] - ElementCenter[1]
                    if RelativePoint[0] < 0:
                        RelativePoint[0] = RelativePoint[0] - RobotRadius
                    else:
                        RelativePoint[0] = RelativePoint[0] + RobotRadius
                    if RelativePoint[1] < 0:
                        RelativePoint[1] = RelativePoint[1] - RobotRadius
                    else:
                        RelativePoint[1] = RelativePoint[1] + RobotRadius
                    Point[0] = ElementCenter[0] + RelativePoint[0]
                    Point[1] = ElementCenter[1] + RelativePoint[1]
                    VirtualElement["Points"].append(Point)
                if "InteractiveFaces" in CopiedMapData["Elements"][Element]:
                    VirtualElement["InteractiveFaces"] = []
                    for Face in CopiedMapData["Elements"][Element]["InteractiveFaces"]:
                        VirtualFace = []
                        for Point in Face:
                            VirtualFace.append(Point)
                        VirtualElement["InteractiveFaces"].append(VirtualFace)
                if "InteractiveSides" in CopiedMapData["Elements"][Element]:
                    VirtualElement["InteractiveSides"] = CopiedMapData["Elements"][Element]["InteractiveSides"]
                VirtualElements["Virtual{0}".format(Element)] = VirtualElement
    for Element in VirtualElements:
        MapData["Elements"][Element] = VirtualElements[Element]
    return MapData

def GetIntersectionPoint(LineOne, LineTwo, LineSegments=True):
    """
    Determines and returns the intersection point of two line segments.
    Returns False if the line segments do not intersect.
    Can be called with "LineSegments = False" to calculate the intersections of unbounded lines.
    """
    X1, Y1, X2, Y2, X3, Y3, X4, Y4 = LineOne[0][0], LineOne[0][1], LineOne[1][0], LineOne[1][1], LineTwo[0][0], LineTwo[0][1], LineTwo[1][0], LineTwo[1][1]
    UaNumerator = ((X4 - X3) * (Y1 - Y3) - (Y4 - Y3) * (X1 - X3))
    UaDenominator = ((Y4 - Y3) * (X2 - X1) - (X4 - X3) * (Y2 - Y1))
    UbNumerator = ((X2 - X1) * (Y1 - Y3) - (Y2 - Y1) * (X1 - X3))
    UbDenominator = ((Y4 - Y3) * (X2 - X1) - (X4 - X3) * (Y2 - Y1))
    if UaNumerator == 0 and UaDenominator == 0 and UaNumerator == 0 and UbDenominator == 0: # If the lines are coincident.
        return False
    elif UaDenominator == 0 and UbDenominator == 0: # If the lines are parallel.
        return False
    else:
        Ua = UaNumerator / UaDenominator
        Ub = UbNumerator / UbDenominator
        X = X1 + Ua * (X2 - X1)
        Y = Y1 + Ua * (Y2 - Y1)
        IntersectionPoint = (X, Y)
        if not LineSegments: # If they are lines.
            return IntersectionPoint
        elif 0 <= Ua <= 1 and 0 <= Ub <= 1: # If they are line segments and they intersect:
            return IntersectionPoint

def ParseInstructions(Instructions):
    """
    Parses and returns pathing instructions.
    """
    Log("Parsing pathing instructions.", 0)
    SplitInstructions = Instructions.split(";")
    ParsedInstructions = {"CurrentPosition": (int(SplitInstructions[0]), int(SplitInstructions[1])), "CurrentRotation": int(SplitInstructions[2]), "ElementDistribution": SplitInstructions[3], "PathList": SplitInstructions[4:]}
    return ParsedInstructions

def Path(MapData, CurrentPosition, ElementDistribution, PathList):
    """
    Constructs and returns the optimal path between each destination in PathList, with respect to the elements described in MapData and ElementDistribution.
    """
    Log("Pathing instructions:\r\n                                 - Initial position: {0}\r\n                                 - Element distribution: {1}\r\n                                 - Path list: {2}".format(CurrentPosition, ElementDistribution, PathList), 0)
    PathfindingMapData = deepcopy(MapData)
    PathInformation = []
    TargetPoints = []
    # Parse TargetPoints.
    for PathIndex, Item in enumerate(PathList):
        if Item.lower() in ("deliver", "collect"): # If the item is an action.
            PathInformation.append(Item)
        elif "," in Item: # If the item is a location (pair of coordinates).
            Item = [int(Number) for Number in Item.split(",")]
            if 0 > Item[0] > PathfindingMapData["Size"][0]:
                Log("X value of path coordinate is out of bounds. ({0} != 0 to {1}).".format(Item[0], PathfindingMapData["Size"][0]), 3)
                return
            if 0 > Item[1] > PathfindingMapData["Size"][1]:
                Log("Y value of path coordinate is out of bounds. ({0} != 0 to {1}).".format(Item[1], PathfindingMapData["Size"][1]), 3)
                return
            TargetPoints.append((Item, PathIndex))
        else: # If the item is a pre-defined location, as described in the .map file.
            if not Item in PathfindingMapData["Elements"]:
                Log("Path target \"{0}\" is not described in map file.".format(Element), 3)
                return
            if "InteractiveFaces" in PathfindingMapData["Elements"][Item]:
                FacesToEvaluate = []
                if "InteractiveSides" in PathfindingMapData["Elements"][Item]:
                    if Item == "NearSwitch":
                        if ElementDistribution[0] == "L":
                            for Index in PathfindingMapData["Elements"][Item]["InteractiveSides"]["Left"]:
                                FacesToEvaluate.append(PathfindingMapData["Elements"][Item]["InteractiveFaces"][Index])
                        else:
                            for Index in PathfindingMapData["Elements"][Item]["InteractiveSides"]["Right"]:
                                FacesToEvaluate.append(PathfindingMapData["Elements"][Item]["InteractiveFaces"][Index])
                    elif Item == "Scale":
                        if ElementDistribution[1] == "L":
                            for Index in PathfindingMapData["Elements"][Item]["InteractiveSides"]["Left"]:
                                FacesToEvaluate.append(PathfindingMapData["Elements"][Item]["InteractiveFaces"][Index])
                        else:
                            for Index in PathfindingMapData["Elements"][Item]["InteractiveSides"]["Right"]:
                                FacesToEvaluate.append(PathfindingMapData["Elements"][Item]["InteractiveFaces"][Index])
                    elif Item == "FarSwitch":
                        if ElementDistribution[2] == "L":
                            for Index in PathfindingMapData["Elements"][Item]["InteractiveSides"]["Left"]:
                                FacesToEvaluate.append(PathfindingMapData["Elements"][Item]["InteractiveFaces"][Index])
                        else:
                            for Index in PathfindingMapData["Elements"][Item]["InteractiveSides"]["Right"]:
                                FacesToEvaluate.append(PathfindingMapData["Elements"][Item]["InteractiveFaces"][Index])
                else:
                    FacesToEvaluate = PathfindingMapData["Elements"][Item]["InteractiveFaces"]
                FaceCenters = []
                FaceDistances = []
                for Face in FacesToEvaluate: # Determine the nearest face.
                    FaceCenter = ((Face[0][0] + Face[1][0]) / 2, (Face[0][1] + Face[1][1]) / 2)
                    FaceCenters.append(FaceCenter)
                    Distance = abs(FaceCenter[0] - CurrentPosition[0]) + abs(FaceCenter[1] - CurrentPosition[1])
                    FaceDistances.append(Distance)
                TargetPoints.append((FaceCenters[min(enumerate(FaceDistances), key=itemgetter(1))[0]], PathIndex))
            else:
                Log("Path target \"{0}\" does not have any InteractiveFaces.", 2)
                # Put down a point to path to regardless. (Use the center of the element.)
                X, Y = zip(*PathfindingMapData["Elements"][Item]["Points"])
                Length = len(X)
                TargetPoints.append(((sum(X) / Length, sum(Y) / Length), PathIndex))
    if not TargetPoints: # If no TargetPoints were specified in the PathList:
        Log("No targeted locations were specified in the PathList passed to Pathfinding.Path.", 4)
        raise ValueError("TargetPoints count out-of-bounds.")
    # Convert TargetPoints into proper path steps.
    PathSteps = [[TargetPoints[0][1], [CurrentPosition, [round(Point) for Point in TargetPoints[0][0]]]]] # [[PathInformationIndex, [Point1, Point2]], ...]
    TargetPointsEvaluated = 1
    while TargetPointsEvaluated < len(TargetPoints):
        PathSteps.append([TargetPoints[TargetPointsEvaluated][1], [[round(Point) for Point in TargetPoints[TargetPointsEvaluated - 1][0]], [round(Point) for Point in TargetPoints[TargetPointsEvaluated][0]]]])
        TargetPointsEvaluated += 1
    # Perform Anya pathfinding for each step of the path.
    StepsEvaluated = 0
    GridData = RasterizeMapData(PathfindingMapData)
    while StepsEvaluated < len(PathSteps):
        StartPoint = PathSteps[StepsEvaluated][1][0]
        EndPoint = PathSteps[StepsEvaluated][1][1]
        StepPoints = [StartPoint]
        StepPoints.extend(Anya(GridData, StartPoint, EndPoint))
        StepPoints.append(EndPoint)
        StepsEvaluated += 1
        Log("Pathfinding complete for step {0} of {1}.".format(StepsEvaluated, len(PathSteps)), 0)
    Log("Pathfinding complete.", 0)
    # Return a list of points that make up the path, along with actions to be taken. Formatted as a tuple:
    # [((X, Y), (X, Y)), "DELIVER", ((X, Y)), "COLLECT", ((X, Y), (X, Y)), "DELIVER"]
    return PathInformation

def RasterizeMapData(MapData):
    """
    Converts MapData to raster format. Every point in the element is described, as opposed to the original format containing just corners.
    """
    Log("Converting MapData from Vector to Raster format.", 0)
    RasterMapData = []
    # Create blank grid.
    I = 0
    while I != MapData["Size"][1] + 1:
        RasterMapData.append([0, ] * (MapData["Size"][0] + 1))
        I += 1
    # Add polygonal MapData elements to the grid.
    for Element in  MapData["Elements"]:
        if MapData["Elements"][Element]["Solidity"] > 0:
            Log("Rasterizing element \"{0}\".".format(Element), 0)
            PairsConverted = 0
            while PairsConverted != len(MapData["Elements"][Element]["Points"]):
                if PairsConverted == 0:
                    PointOne, PointTwo = MapData["Elements"][Element]["Points"][len(MapData["Elements"][Element]["Points"]) - 1], MapData["Elements"][Element]["Points"][0] # The first pair will be the last item in the list --> the first item in the list.
                else:
                    PointOne, PointTwo = MapData["Elements"][Element]["Points"][PairsConverted - 1], MapData["Elements"][Element]["Points"][PairsConverted]
                PairPoints = BresenhamLinePoints(PointOne, PointTwo)
                for Point in PairPoints:
                    RasterMapData[Point[1]][Point[0]] = 1
                PairsConverted += 1
    return RasterMapData

def VectorizePathInformation(PathInformation):
    """
    Converts each pair of destination points into a vector with an offset in degrees from the previous line, and a length.
    """
    return PathInformation

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")

# TODO: ALL of this program should eventually be converted to use the "Point" namedtuple!!! See Anya.py for more information on that variable.
