# -*- coding: utf8 *-*

#
# Built-in imports.
#

from collections import namedtuple
from math import acos, degrees, hypot
import operator
import sys
import time

#
# Custom imports.
#

from RenderAnya import RenderAnya # TODO: Change this into the proper Render import once testing on Anya is completed.

#
# Global variables.
#

Point = namedtuple("Point", "X Y")

#
# Functions.
#

def Anya(GridData, TupleStartPoint, TupleEndPoint):
    """
    Finds the optimal path between two points on a grid. Returns tuple with each point in the path. Returns False if no path exists.
    Anya implementation based on the paper "Optimal Any-angle Pathfinding in Practice", published in the Journal of Artificial Intelligence Research (JAIR); written by D. Harabor, A. Grastien, D. Öz and V. Aksakalli; 2016.
    """
    #
    # Function variables.
    #

    GridHeight = len(GridData) - 1
    GridWidth = len(GridData[0]) - 1
    Interval = namedtuple("Interval", "StartFlag StartPoint EndPoint EndFlag")
    Node = namedtuple("Node", "Interval Root") # These two keys - Interval and Root - must be in the type of the namedtuples Interval and Point, respectively.
    EndPoint = Point(TupleEndPoint[0], TupleEndPoint[1])
    RootHistory = []
    StartPoint = Point(TupleStartPoint[0], TupleStartPoint[1])

    #
    # Sub-functions.
    #

    def FareySequence(N, Descending = False):
        """
        Calculate the Farey Sequence of order N.
        """
        # N needs to be min(Width, Height)
        FareySequence = []
        A, B, C, D = 0, 1, 1, N
        if Descending:
            A, C = 1, N - 1
        FareySequence.append(A, C)
        while (C <= N and not Descending) or (A > 0 and Descending):
            K = int((N + B) / D)
            A, B, C, D = C, D, (K * C - A), (K * D - B)
            FareySequence.append(A, B)
        return FareySequence

    def FarthestPoint(ReferencePoint, *OtherPoints):
        """
        Returns the Point which is farthest from the ReferencePoint passed.
        """
        for Point in OtherPoints:
            MaximumValueIndex, MaximumValue = max(enumerate([hypot(Point.X - ReferencePoint.X, Point.Y - ReferencePoint.Y) for Point in OtherPoints]), key=operator.itemgetter(0))
            return OtherPoints[MaximumValueIndex], MaximumValue


    def FValue(Node): # TODO: Complete this function.
        """
        Calculate the F value of a Node.
        """


    def GenerateSuccessors(Node):
        """
        Generates the successors of an Anya search node.
        """
        def GenerateConeSuccessors(PointOne, PointTwo, Root):
            """
            Generates the successors of a cone search node.
            """
            pass

        def GenerateFlatSuccessors(PointOne, Root):
            """
            Generates the successors of a flat search node.
            """
            PointTwo = None # TODO: This point must be the first corner point (or otherwise the farthest obstacle vertex) on the row of PointOne such that "Root --> PointOne --> PointTwo" is taut.

        def GenerateStartSuccessors(StartPoint):
            """
            Generates the successors for the start search node.
            """
            # Construct a maximal half-closed interval containing all points observable and to the left of StartPoint. (This does not include the StartPoint itself.)
            LeftStartInterval = []
            if LineOfSight(StartPoint, [0, StartPoint.Y]):
                LeftStartInterval = Interval(True, Point(0, StartPoint.Y), StartPoint, False)
            else:
                LeftPoints = BresenhamLinePoints(StartPoint, Point(0, StartPoint.Y))
                for Point, PointIndex in enumerate(LeftPoints):
                    if GridData(Point.X, Point.Y) == 1:
                        LeftStartInterval = Interval(True, LeftPoints[PointIndex], StartPoint, False)
            # Construct a maximal half-closed interval containing all points observable and to the right of StartPoint. (This does not include the StartPoint itself.)
            RightStartInterval = []
            if LineOfSight(StartPoint, Point(GridWidth, StartPoint.Y)):
                RightStartInterval = Interval(False, StartPoint, Point(GridWidth, StartPoint.Y))
            else:
                RightPoints = BresenhamLinePoints(StartPoint, Point(GridWidth, StartPoint.Y))
                for Point, PointIndex in enumerate(RightPoints):
                    if GridData(Point.X, Point.Y) == 1:
                        RightStartInterval = Interval(False, StartPoint, RightPoints[PointIndex], True)
            # Construct a maximal half-closed interval containing all points observable and from the row above StartPoint.
            UpperLeftPoints = BresenhamLinePoints(Point(0, StartPoint.Y + 1), Point(StartPoint.X, StartPoint.Y + 1))
            UpperRightPoints = BresenhamLinePoints(Pont(StartPoint.X, StartPoint.Y + 1), Point(GridWidth, StartPoint.Y + 1))
            if LineOfSight(StartPoint, Point(0, StartPoint.Y + 1)): # If there is a LOS from the Root to the leftmost point in the upper row.
                UpperStartIntervalLeft = [True, Point(0, StartPoint.Y + 1)]
            else: # Scan left until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperLeftPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalLeft = [True, UpperLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, Point(GridWidth, StartPoint.Y + 1)): # If there is a LOS from the Root to the rightmost point in the upper row.
                UpperStartIntervalRight = [Point(GridWidth, StartPoint.Y + 1), True]
            else: # Scan right until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperRightPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalRight = [UpperRightPoints[PointIndex - 1], True]
            UpperStartInterval = Interval(UpperStartIntervalLeft + UpperStartIntervalRight) # TODO: Determine if this unpacks naturally into StartFlag, StartPoint, EndPoint, EndFlag...
            # Construct a maximal half-closed interval containing all points observable and from the row below StartPoint.
            LowerLeftPoints = BresenhamLinePoints(Point(0, StartPoint.Y - 1), Point(StartPoint.X, StartPoint.Y - 1))
            LowerRightPoints = BresenhamLinePoints(Point(StartPoint.X, StartPoint.Y - 1), Point(GridWidth, StartPoint.Y - 1))
            if LineOfSight(StartPoint, Point(0, StartPoint.Y - 1)): # If there is a LOS from the Root to the leftmost point in the lower row.
                LowerStartIntervalLeft = [True, Point(0, StartPoint.Y - 1)]
            else: # Scan left until we no longer have a LOS.
                for Point, PointIndex in enumerate(LowerLeftPoints):
                    if not LineOfSight(StartPoint, Point):
                        LowerStartIntervalLeft = [True, LowerLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, Point(GridWidth, StartPoint.Y - 1)):
                LowerStartIntervalRight = [Point(GridWidth, StartingPoint.Y - 1), True]
            else: # Scan right until we no longer have a LOS.
                for Point, PointIndex in enumerate(LowerRightPoints):
                    if not LineOfSight(StartPoint, Point):
                        LowerStartIntervalRight = [LowerRightPoints[PointIndex - 1], True]
            LowerStartInterval = Interval(LowerStartIntervalLeft + LowerStartIntervalRight) # TODO: Determine if this unpacks naturally into StartFlag, StartPoint, EndPoint, EndFlag...
            # Split each interval at any corner points.
            Intervals = [SplitInterval(LeftStartInterval), SplitInterval(RightStartInterval), SplitInterval(UpperStartInterval), SplitInterval(LowerStartInterval)]
            Log("Anya Intervals for Root {0} created at {1}.".format(Root, Intervals), 0)
            StartSuccessors = [GenerateSuccessors(Node(Interval, StartPoint)) for Interval in Intervals]
            return StartSuccessors

        NodeType = NodeType(Node)
        if NodeType == "START":
            Successors = GenerateStartSuccessors(StartPoint)
        elif NodeType == "FLAT":
            FarPoint = FarthestPoint(Interval.StartPoint, Interval.EndPoint) # TODO: Determine which Point in the Interval is farthest from the Node's Root.
            Successors = GenerateFlatSuccessors() # The Point passed is the Point in the Interval which is farthest from the Node's Root.
            if IsTurningPoint(FarPoint): # TODO: Determine if FarPoint is a turning point on a taut local path beginning at Node.Root.
                Successors = Successors.union(GenerateConeSuccessors(FarPoint, FarPoint, Node.Root)) # These are non-observable successors.
        else: # NodeType == "CONE"
            Successors = GenerateConeSuccessors(Node.Interval.PointTwo, Node.Interval.PointOne, Node.Root)

    def GridData(X, Y):
        """
        Provides an easy to determine the value of a specific coordinate in the grid.
        """
        return GridData[Y][X]

    def IsTaut(PointOne, PointTwo, PointThree):
        """
        Determines if a sequence of three points is taut; that is, if their angles equal 180 degrees. Returns True if taut, otherwise returns false.
        """
        A = hypot(PointTwo.X - PointOne.X, PointTwo.Y - PointOne.Y) # Distance from PointOne to PointTwo.
        B = hypot(PointThree.X - PointTwo.X, PointThree.Y - PointTwo.Y) # Distance from PointTwo to PointThree.
        C = hypot(PointOne.X - PointThree.X, PointOne.Y - PointThree.Y) # Distance from PointThree to PointOne (hypotenuse).
        Angle = degrees(acos(A * A + B * B - C * C) / (2 * A * B))
        if Angle == 180:
            return True

    def IsTurningPoint(): # TODO: Complete this function.
        """
        WIP.
        """
        return

    def LiesWithin(Point, Interval): # TODO: Complete this function.
        """
        Determines whether a point lies within an interval.
        """
        IntervalPoints = BresenhamLinePoints(Interval.StartPoint, Interval.EndPoint)

    def LineOfSight(PointOne, PointTwo):
        """
        Determines whether two points have a line-of-sight; that is, if a line drawn between them does not intersect with any solid (non-traversable) points.
        """
        LinePoints = BresenhamLinePoints(PointOne, PointTwo)

        if any(GridData[Point[1]][Point[0]] for Point in LinePoints) == 1:
            return False

    def NodeType(Node):
        """
        Determines and returns the type of an Anya search node.
        """
        Interval, Root = Node
        if Root == Point(-1, -1): # If the root of the node is off the map.
            return "START"
        elif Root.Y != Interval.StartPoint.Y and Root.Y != Interval.EndPoint.Y: # If the root of the node is not on the same line (does not have the same Y value) as the points contained in the Interval.
            return "CONE"
        elif Root.Y == Interval.StartPoint.Y and Root.Y == Interval.EndPoint: # If the root of the node is on the same line as the (has the same Y value) as the points contained in the Interval.
            return "FLAT"

        def ProjectNode(Node): # TODO: Complete this function.
            """
            Computes and returns the maximum observable interval projection for the node passed.
            If the projection is invalid, returns False.
            """
            if NodeType(Node) == "FLAT":
                pass
            elif NodeType(Node) == "CONE":
                Interval, Root = Node
                if EndPoint.Y > Root.Y: # Project up, because the EndPoint is above the root.
                    pass
                elif EndPoint.Y < Root.Y: # Project down, because the EndPoint is below the root.
                    pass

        def ShouldPrune(Node): # TODO: Complete this function.
            """
            Determines whether an Anya search Node should be pruned.
            """
            def IsCulDeSac(Node):
                """
                Determines whether an Anya search Node is a "Cul De Sac".
                """
                ProjectedInterval = ProjectNode(Node)
                if ProjectedInterval: # If the ProjectedInterval is valid.
                    return False
            def IsIntermediate(Node):
                """
                Determines whether an Anya search Node is an intermediate Node.
                """
                if NodeType(Node) == "FLAT":
                    FarPoint = None # TODO: Determine which Point in the Interval is farthest from the Node's Root.
                    if IsTurningPoint(FarPoint): # If FarPoint is a turning point for a taut local path with prefix (Root, Point), then the Node must have at least one non-observable successor; it cannot be intermediate.
                        return False
                else: # The Node is not a flat node; therefore it must be a cone noe.
                    if Interval: # TODO: "If Interval has a closed endpoint that is also a corner point..."
                        return False
                    ProjectedInterval = ProjectNode(Node)
                    if ProjectedInterval: # TODO: "If ProjectedInterval contains any corner points..."
                        return False
                return True

        def SplitInterval(Interval, ReturnUnsplitInterval=False): # TODO: Complete this function.
            """
            Splits an Interval at any corner points into a new interval. Returns a tuple containing any new intervals. If no new intervals were created, returns False. (Call with "ReturnUnsplitInterval" = "True" to return the original interval if it was not split.)
            """
            Intervals = []
            return Intervals

    #
    # Mainline function code.
    #

    StepPathData = []
    StartInterval = Interval(True, StartPoint, StartPoint, True)
    return StepPathData

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

#
# Mainline code.
#

######################################################
#                                                    #
#                                                    #
#                                                    #
# TODO: Remove all of this once testing is complete! #
#                                                    #
#                                                    #
#                                                    #
######################################################

print("ANYA testing!")
#MapFile = input("Please enter map file name: ")
#Sx = input("Please enter X pos. of StartPoint: ")
#Sy = input("Please enter Y pos. of StartPoint: ")
#Ex = input("Please enter X pos. of EndPoint: ")
#Ey = input("Please enter Y pos. of EndPoint: ")
#StartPoint = [Sx, Sy]
#EndPoint = [Ex, Ey]

MapFile = "temp.map"
TupleStartPoint = [95, 10]
TupleEndPoint = [5, 30]

GridData = []

with open(MapFile, "r") as File:
    GridData = File.readlines()[::-1] # We reverse and make a shallow copy of the list.

GridData = [list(Line.strip()) for Line in GridData] # Remove newlines.
for LineIndex, Line in enumerate(GridData):
    for CharacterIndex, Character in enumerate(GridData[LineIndex]):
        GridData[LineIndex][CharacterIndex] = int(Character) # Split each line character-by-character, and convert each character from a string into an integer.

print("Map loaded! Filename: \"{0}\". Map dimensions: {1} * {2}.".format(MapFile, len(GridData[0]), len(GridData)))
RenderAnya(GridData)

StartTime = time.time()
StepPathData = Anya(GridData, TupleStartPoint, TupleEndPoint)
EndTime = time.time()
RunTime = EndTime - StartTime

print("Anya complete! Estimated run time: {0}.".format(RunTime))

def ClonedFarthestPoint(ReferencePoint, *OtherPoints):
    """
    Returns the Point which is farthest from the ReferencePoint passed.
    """
    for Point in OtherPoints:
        print("Point in OtherPoints: \"{0}\"".format(Point))
    print("ReferencePoint: \"{0}\"".format(ReferencePoint))
    MaximumValueIndex, MaximumValue = max(enumerate([hypot(Point.X - ReferencePoint.X, Point.Y - ReferencePoint.Y) for Point in OtherPoints]), key=operator.itemgetter(0))
    MaximumValuePoint = OtherPoints[MaximumValueIndex]
    return MaximumValuePoint, MaximumValue