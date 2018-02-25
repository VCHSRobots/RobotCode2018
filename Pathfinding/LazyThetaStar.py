from collections import namedtuple

from Log import Log
from RenderAnya import RenderAnya

Point = namedtuple("Point", "X Y")

ParentsTable = {}
LineOfSightChecks = 0

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
        Coordinate = Point(Y, X) if IsSteep else Point(X, Y)
        Points.append(Coordinate)
        Error -= abs(DY)
        if Error < 0:
            Y += YStep
            Error += DX
    if Swapped:
        Points.reverse()
    return Points

def Main(StartPoint, EndPoint):
    """
    The main function for Lazy Theta *.
    """
    Open = []
    Closed = []

    SetParent(StartPoint, StartPoint)
    while Open:
        CurrentPoint = Open.pop()
        SetVertex(CurrentPoint)


def GetGridData(X, Y):
    """
    Return the value of a specific coordinate.
    """
    return GridData[Y - 1][X - 1]

def GetNeighbors(ReferancePoint):
    """
    Return the values of the eight neighboring verticies.
    """
    return None

def GetGValue(FinalPoint):
    """
    Return the G-value of StartPoint -> Parent(s) -> FinalPoint.
    """
    return None

def GetParents(InitialPoint, OnlyDirectParent=False):
    """
    Returns all of the parents a point may have. Call with "OnlyDirectParent=True" to return only the immediate parent.
    """
    return

def LineOfSight(PointOne, PointTwo):
    """
    Determines whether two points have a line-of-sight; that is, if a line drawn between them does not intersect with any solid (non-traversable) points.
    """
    LinePoints = BresenhamLinePoints(PointOne, PointTwo)
    if any(GetGridData(LinePoint.X, LinePoint.Y) for LinePoint in LinePoints) == 1:
        return False

def SetParent(InitialPoint, ParentPoint):
    """
    Sets the parent of Initial Point as ParentPoint in the ParentsTable.
    """
    ParentsTable[InitialPoint] = ParentPoint

def SetVertex():
    if not LineOfSight(GetParent)

def UpdateVertex():
    """
    Update a vertex.
    """

#
# Temporary mainline test code...
#

print("Lazy Theta * testing!")

MapFile = "test3.map"
StartPoint = Point()
EndPoint = Point()

print("Map loaded! Filename: \"{0}\". Map dimensions: {1} * {2}.".format(MapFile, len(GridData[0]), len(GridData)))
RenderAnya(GridData, "_LazyThetaStarRender GridData")

StartTime = time.time()
Path = Main(StartPoint, EndPoint)
EndTime = time.time()

print("\"Lazy Theta *\" complete! Estimated run time: {0}.".format(EndTime - StartTime))

if not Path:
    print("No path found! :(")
    return
print("A path was found! See \"Renders/\".")