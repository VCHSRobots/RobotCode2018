 # -*- coding: utf8 -*-

"""Pathfinding.py

Pathfinding.py calculates the shortest path for the robot between it's current location and any number of locations.
"""

#
# Built-in imports.
#

from copy import deepcopy
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

def ExpandMapElements(MapData):
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
                        for Point in Face: # TODO: Simplify FOR statements.
                            # TODO: Do this!
                            VirtualFace.append(Point)
                        VirtualElement["InteractiveFaces"].append(VirtualFace)
                if "InteractiveSides" in CopiedMapData["Elements"][Element]:
                    VirtualElement["InteractiveSides"] = CopiedMapData["Elements"][Element]["InteractiveSides"]
                VirtualElements["Virtual{0}".format(Element)] = VirtualElement
    for Element in VirtualElements:
        MapData["Elements"][Element] = VirtualElements[Element]
    return MapData

def GetNearestActionableElementFace():
    pass

def GetIntersectionPoint(LineOne, LineTwo, LineSegments = True): # Returns False if line segments do not intersect. Otherwise returns coordinate of intersection point. Call with "LineSegments" as False to calculate the intersections of unbounded lines.
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
        if not LineSegments:
            return IntersectionPoint
        elif 0 <= Ua <= 1 and 0 <= Ub <= 1: # If they are line segments and they intersect:
            return IntersectionPoint
        else: # If they are line segments and they do not intersect:
            return False


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
    PathfindingMapData = deepcopy(MapData)
    PathInformation = []
    TargetPoints = []
    for PathIndex, Item in enumerate(PathList):
        if Item.lower() in ("deliver", "collect"): # If the item is an action.
            PathInformation.append(Item)
        elif len(Item) == 2: # If the item is a location (pair of coordinates).
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
    LinesEvaluated = 0
    for Index, Point in enumerate(TargetPoints): # Evaluate the shortest path between the current location and each of the points listed.
        StartPoint = []
        EndPoint = []
        PathPoints = []
        if LinesEvaluated == 0:
            StartPoint = CurrentPosition
            EndPoint = TargetPoints[0][0]
        else:
            StartPoint = TargetPoints[LinesEvaluated - 1][0]
            EndPoint = TargetPoints[LinesEvaluated][0]
        # Filter out possible intersections with elements by only searching for ones which have a solidity greater than or equal to 1 and exist within the quadrant of the vector's direction.
        Angle = round(math.degrees(math.atan2(EndPoint[1] - StartPoint[1], EndPoint[0] - StartPoint[0])))
        if Angle < 0:
            Angle = 360 + Angle
        StepQuadrants = GetQuadrants(Angle)
        if len(StepQuadrants) > 1:
            Plural = "s"
        else:
            Plural = ""
        Log("Pathfinding started for step {0}. Step starts at point \"{1}\" and ends at point \"{2}\", and has an angle of {3}°, therefore extending into quadrant{4} {5}.".format(LinesEvaluated + 1, StartPoint, EndPoint, Angle, Plural, StepQuadrants), 0)
        SolidElements = []
        for Element in PathfindingMapData["Elements"]:
            if PathfindingMapData["Elements"][Element]["Solidity"] >= 1:
                SolidElements.append(Element)
        ElementsToEvaluate = []
        for Element in SolidElements:
            if any(GetQuadrants(round(math.degrees(math.atan2(Point[1] - StartPoint[1], Point[0] - StartPoint[0])))) == StepQuadrants for Point in PathfindingMapData["Elements"][Element]["Points"]): # If any of the element's points exist within the proper quadrant(s).
               ElementsToEvaluate.append(Element)
        StartPoint = [int(Coordinate) for Coordinate in StartPoint]
        PathPoints.append(list(StartPoint))
        Log("Pathfinding is evaluating potential element intersections for path step {0}.".format(LinesEvaluated + 1), 0)
        ElementIntersections = []
        for Element in ElementsToEvaluate:
            Log("Pathfinding is evaluating intersections with element \"{0}\".".format(Element), 0)
            ElementLinesEvaluated = 0
            while ElementLinesEvaluated < len(PathfindingMapData["Elements"][Element]["Points"]) - 1:
                LineOne = (StartPoint, EndPoint)
                LineTwo = (PathfindingMapData["Elements"][Element]["Points"][ElementLinesEvaluated], PathfindingMapData["Elements"][Element]["Points"][ElementLinesEvaluated + 1])
                IntersectionPoint = GetIntersectionPoint(LineOne, LineTwo)
                if IntersectionPoint:
                    Distance = math.hypot(IntersectionPoint[0] - LineOne[0][0], IntersectionPoint[1] - LineOne[0][1])
                    ElementIntersections.append((Element, IntersectionPoint, Distance))
                ElementLinesEvaluated += 1
        if len(ElementIntersections) == 0:
            Log("Pathfinding found no intersections with element \"{0}\"".format(Element), 0)
        elif len(ElementIntersections) > 0:
            ElementIntersections = sorted(ElementIntersections, key=itemgetter(2))
            print(str(ElementIntersections)) # TODO: TEMP
            IntersectedElement, ClosestIntersectionPoint, Distance = ElementIntersections[0][0], [round(Number) for Number in ElementIntersections[0][1]], round(ElementIntersections[0][2]) # Sort element intersections by distance, and keep the coordinates of the closest intersection.
            Plural = ""
            if len(ElementIntersections) > 1:
                Plural = "s"
            Log("Pathfinding found {0} intersection{1}. The closest intersection was at point \"{2}\" with element {3}".format(len(ElementIntersections), Plural, ClosestIntersectionPoint, IntersectedElement), 0)
        EndPoint = [int(Coordinate) for Coordinate in EndPoint]
        PathPoints.append(list(EndPoint))
        Log("Pathfinding completed for step {0} of {1}".format(LinesEvaluated + 1, len(TargetPoints)), 0)
        LinesEvaluated += 1
        PathInformation.insert(TargetPoints[Index][1], list(PathPoints)) # TODO: Update this.
    Log("Pathfinding complete.", 0)
    # Return a list of points that make up the path, along with actions to be taken. Formatted as a tuple:
    # [(X, Y), (X, Y), "DELIVER", (X, Y), "COLLECT", (X, Y), (X, Y), "DELIVER"]
    return PathInformation

def VectorizePathInformation(PathInformation):
    pass
    return PathInformation

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
