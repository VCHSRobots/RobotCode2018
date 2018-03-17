from collections import namedtuple
import math
import operator
import time

from RenderAnya import RenderAnya

Point = namedtuple("Point", "X Y")

ParentsTable = {}
GValueTable = {}
Open = {} # Open's format: Point: Value, Point2: Value, ...
Closed = []
LineOfSightChecks = 0

def BresenhamLinePoints(PointOne, PointTwo):
    """
    Returns every point that lies along the line created by the StartPoint and the EndPoint.
    Algorithm based on the example at http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python.
    """
    X1, Y1 = [int(round(Number)) for Number in PointOne]
    X2, Y2 = [int(round(Number)) for Number in PointTwo]
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
        Coordinate = Point(Y, X) if IsSteep else Point(X, Y)
        Points.append(Coordinate)
        Error -= abs(DY)
        if Error < 0:
            Y += YStep
            Error += DX
    if Swapped:
        Points.reverse()
    return Points

def ComputeCost(PointOne, PointTwo):
    if LineOfSight(GetParents(PointOne, True), PointTwo):
        # Path 2
        if GetGValue(GetParents(PointOne, True)) + GetDistance(GetParents(PointOne, True), PointTwo) < GetGValue(PointTwo):
            SetParent(PointTwo, GetParents(PointOne, True))
            Val = GetGValue(GetParents(PointOne, True)) + GetDistance(GetParents(PointOne, True), PointTwo)
            SetGValue(PointTwo, Val)
    else:
        # Path 1
        if GetGValue(PointOne) + GetDistance(PointOne, PointTwo) < GetGValue(PointTwo):
            SetParent(PointTwo, PointOne)
            Val = GetGValue(PointOne) + GetDistance(PointOne, PointTwo)
            SetGValue(PointTwo, Val)

def Main(StartPoint, EndPoint):
    """
    The main function for Lazy Theta *.
    """
    global Closed
    global Open
    SetParent(StartPoint, StartPoint)
    Open[StartPoint] = GetGValue(StartPoint) + GetDistance(StartPoint, StartPoint)
    while Open:
        print("Open is:\r\n{0}".format(Open)) # TODO: TEMP
        CurrentPoint = sorted(Open, key=Open.__getitem__)[0] # Get the point with the lowest key value (in this case, that refers to the distance).
        print("CurrentPoint is \"{0}\"".format(CurrentPoint)) # TODO: TEMP
        # SetVertex(CurrentPoint)
        if CurrentPoint == EndPoint:
            return "Path found!"
        Closed = list(set(Closed) | set(CurrentPoint))
        for NeighborPointWithLOS in GetNeighborsWithLOS(CurrentPoint): # Neighbors of point "S" which have LOS to "S".
            if NeighborPointWithLOS not in Closed:
                if NeighborPointWithLOS not in Open:
                    SetGValue(NeighborPointWithLOS, math.inf)
                    SetParent(NeighborPointWithLOS, None)
                    print("An orphan has been born ;_;")
                UpdateVertex(CurrentPoint, NeighborPointWithLOS)
    return

def GetDistance(PointOne, PointTwo):
    """
    Returns the distance from PointOne to PointTwo, multiplied by the HeuristicWeight.
    """
    if PointOne == None or PointTwo == None:
        return 0
    return HeuristicWeight * math.hypot(PointTwo.X - PointOne.X, PointTwo.Y - PointOne.Y)

def GetGridData(X, Y):
    """
    Return the value of a specific coordinate.
    """
    return GridData[Y - 1][X - 1]

def GetNeighbors(ReferancePoint):
    """
    Return the values of the eight neighboring verticies.
    """
    return [Point(ReferancePoint.X + 1, ReferancePoint.Y + 1), Point(ReferancePoint.X, ReferancePoint.Y + 1), Point(ReferancePoint.X - 1, ReferancePoint.Y + 1), Point(ReferancePoint.X - 1, ReferancePoint.Y), Point(ReferancePoint.X - 1, ReferancePoint.Y - 1), Point(ReferancePoint.X, ReferancePoint.Y - 1), Point(ReferancePoint.X + 1, ReferancePoint.Y - 1), Point(ReferancePoint.X + 1, ReferancePoint.Y)]

def GetNeighborsWithLOS(ReferancePoint):
    """
    Returns all neighbor points of the ReferancePoint with a line-of-sight to the ReferancePoint.
    """
    return [NeighborPoint for NeighborPoint in GetNeighbors(ReferancePoint) if LineOfSight(ReferancePoint, NeighborPoint)]

def GetGValue(FinalPoint):
    """
    Return the G-value of StartPoint -> Parent(s) -> FinalPoint.
    """
    return GetDistance(StartPoint, GetParents(FinalPoint, True)) + GetDistance(GetParents(FinalPoint, True), FinalPoint)

def GetParents(InitialPoint, GetOnlyDirectParent=False):
    """
    Returns all of the parents a point may have. Call with "OnlyDirectParent=True" to return only the immediate parent.
    """
    if GetOnlyDirectParent:
        return ParentsTable[InitialPoint]
    else: # Not implemented yet! TODO: Implement this.
        return

def LineOfSight(PointOne, PointTwo):
    """
    Determines whether two points have a line-of-sight; that is, if a line drawn between them does not intersect with any solid (non-traversable) points.
    """
    LinePoints = BresenhamLinePoints(PointOne, PointTwo)
    if any(GetGridData(LinePoint.X, LinePoint.Y) for LinePoint in LinePoints) == 1:
        return False
    else:
        return True

def SetGValue(InitialPoint, GValue):
    """
    Sets the G Value of a point.
    """
    GValueTable[InitialPoint] = GValue

def SetParent(InitialPoint, ParentPoint):
    """
    Sets the parent of Initial Point as ParentPoint in the ParentsTable.
    """
    print("Parent of {0} set to {1}.".format(InitialPoint, ParentPoint)) # TODO: TEMP
    ParentsTable[InitialPoint] = ParentPoint

""" 
def SetVertex(InitialPoint):
     if not LineOfSight(GetParents(InitialPoint, True), InitialPoint):
        # Path 1.
        NeighborsWithLOS = [LePoint for LePoint in GetNeighborsWithLOS(InitialPoint).union(Closed)]
        NeighborsWithLOS = list(set(NeighborsWithLOS) & set(Closed))
        NeighborIndex, Neighbor = min([GetGValue(Neighbor) + GetDistance(Neighbor, InitialPoint) for NeighborIndex, Neighbor in enumerate(NeighborsWithLOS)], key=operator.itemgetter(1))
        SetParent(InitialPoint, NeighborsWithLOS[NeighborIndex])
        GValue = GetGValue(Neighbor) + GetDistance(Neighbor, InitialPoint)
        SetGValue() 
"""

def UpdateVertex(PointOne, PointTwo):
    """
    Update a vertex.
    """
    global Open
    OldGValue = GetGValue(PointTwo)
    ComputeCost(PointOne, PointTwo)
    print("OldGValue: {0}; NewGValue: {1}.".format(OldGValue, GetGValue(PointTwo)))
    if GetGValue(PointTwo) < OldGValue:
        if PointTwo in Open:
            print("Open:\r\n {0}.".format(Open)) # TODO: TEMP
            del Open[PointTwo]
            print("Open updated 1:\r\n {0}.".format(Open)) # TODO: TEMP
        Open[PointTwo] = GetGValue(PointTwo) + GetDistance(PointTwo, EndPoint)
        print("Open updated 2:\r\n {0}.".format(Open)) # TODO: TEMP

#
# Temporary mainline test code...
#

print("Lazy Theta * testing!")

# Fancy variables that the user can edit!

MapFile = "test3.map"
StartPoint = Point(175, 35)
EndPoint = Point(1000, 875)
HeuristicWeight = 1 # 1 is the default. Change to 1.1 for optimization testing; finds (slightly) longer paths with a (slight) decrease in runtime.

# Resume normal temporary mainline code.

GridData = []
with open(MapFile, "r") as File:
    GridData = File.readlines()[::-1] # We reverse and make a shallow copy of the list.
GridData = [list(Line.strip()) for Line in GridData] # Remove newlines.
for RowIndex, Row in enumerate(GridData):
    for CharacterIndex, Character in enumerate(GridData[RowIndex]):
        GridData[RowIndex][CharacterIndex] = int(Character) # Split each line character-by-character, and convert each character from a string into an integer.
print("Map loaded! Filename: \"{0}\". Map dimensions: {1} * {2}.".format(MapFile, len(GridData[0]), len(GridData)))

RenderAnya(GridData, "_LazyThetaStarRender GridData")

StartTime = time.time()
Path = Main(StartPoint, EndPoint)
EndTime = time.time()

print("\"Lazy Theta *\" complete! Estimated run time: {0}.".format(EndTime - StartTime))

if not Path:
    print("No path found. :(")
else:
    print(Path)
    print("See \"Renders/\" for a nice drawing. :)")
