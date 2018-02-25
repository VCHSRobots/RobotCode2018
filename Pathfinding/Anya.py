# -*- coding: utf8 *-*

#
# Built-in imports.
#

from collections import Counter, namedtuple
from math import acos, ceil, degrees, floor, hypot
import operator
import sys
import time

#
# Custom imports.
#

from Log import Log
from RenderAnya import RenderAnya # TODO: Change this into the proper Render import once testing on Anya is completed.

#
# Global variables.
#

Interval = namedtuple("Interval", "StartFlag StartPoint EndPoint EndFlag")
Line = namedtuple("Line", "PointOne PointTwo")
Node = namedtuple("Node", "Interval Root") # These two keys - Interval and Root - must be in the type of the namedtuples Interval and Point, respectively.
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

    EndPoint = Point(TupleEndPoint[0], TupleEndPoint[1])
    GridHeight = len(GridData)
    GridWidth = len(GridData[0])
    RootHistory = []
    StartPoint = Point(TupleStartPoint[0], TupleStartPoint[1])

    #
    # Sub-functions.
    #

    def FareySequence(N, Descending=False):
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
        MaximumDistanceIndex, MaximumDistance = max(enumerate([hypot(OtherPoint.X - ReferencePoint.X, OtherPoint.Y - ReferencePoint.Y) for OtherPoint in OtherPoints]), key=operator.itemgetter(0)) # TODO: Remove MaximumDistance; it is never used.
        return OtherPoints[MaximumDistanceIndex]

    def FValue(PassedNode): # TODO: Simplify this function! We don't need to repeat the code for "FValueEstimate" so many times! Also remove unnecessary / redundant value checks in IF statements! (╯°□°）╯︵ ┻━┻
        """
        Calculate the "F Value" of a Node.
        """
        IntersectionPoint = GetIntersectionPoint(Line(PassedNode.Root, EndPoint), Line(PassedNode.Interval.StartPoint, PassedNode.Interval.EndPoint))
        if IntersectionPoint:
            FValueEstimate = hypot(PassedNode.Root.X - StartPoint.X, PassedNode.Root.Y - StartPoint.Y) + hypot(IntersectionPoint.X - PassedNode.Root.X, IntersectionPoint.Y - PassedNode.Root.Y) + hypot(EndPoint.X - IntersectionPoint.X, EndPoint.Y - IntersectionPoint.Y) # Distance from Source-Root + Root-Point + Point-Target.
        else: # The path from the Root to the EndPoint does not pass through the interval.
            # If the Root and the EndPoint are both below (or above) the interval.
            if PassedNode.Interval.StartPoint.Y - EndPoint.Y > 0 and PassedNode.Interval.StartPoint.Y - PassedNode.Root.Y > 0: # If they are above the Interval.
                YDifference = EndPoint.Y - PassedNode.Interval.StartPoint.Y
                MirroredEndPoint = Point(EndPoint.X, PassedNode.Interval.StartPoint.Y - YDifference)
                FValueEstimate = hypot(PassedNode.Root.X - StartPoint.X, PassedNode.Root.Y - StartPoint.Y) + hypot(IntersectionPoint.X - PassedNode.Root.X, IntersectionPoint.Y - PassedNode.Root.Y) + hypot(MirroredEndPoint.X - IntersectionPoint.X, MirroredEndPoint.Y - IntersectionPoint.Y) # Distance from Source-Root + Root-Point + Point-Target.
            elif PassedNode.Interval.StartPoint.Y - EndPoint.Y < 0 and PassedNode.Interval.StartPoint.Y - PassedNode.Root.Y < 0: # If they are below the Interval.
                YDifference = PassedNode.Interval.StartPoint.Y - EndPoint.Y
                MirroredEndPoint = Point(EndPoint.X, PassedNode.Interval.StartPoint.Y + YDifference)
                FValueEstimate = hypot(PassedNode.Root.X - StartPoint.X, PassedNode.Root.Y - StartPoint.Y) + hypot(IntersectionPoint.X - PassedNode.Root.X, IntersectionPoint.Y - PassedNode.Root.Y) + hypot(MirroredEndPoint.X - IntersectionPoint.X, MirroredEndPoint.Y - IntersectionPoint.Y) # Distance from Source-Root + Root-Point + Point-Target.
            else: # Otherwise, they are on opposite sides of the interval. (This should be the norm.)
                IntersectionPoint = GetIntersectionPoint(Line(PassedNode.Root, EndPoint), Line(PassedNode.Interval.StartPoint, PassedNode.Interval.EndPoint), False) # Where would they intersect if they were lines; not line-segments?
                if IntersectionPoint.X < PassedNode.Interval.StartPoint.X and IntersectionPoint.X < PassedNode.Interval.EndPoint.X: # If the Root-EndPoint line travels to the left of the interval.
                    FValueEstimate = hypot(PassedNode.Root.X - StartPoint.X, PassedNode.Root.Y - StartPoint.Y) + hypot(PassedNode.Interval.StartPoint.X - PassedNode.Root.X, PassedNode.Interval.StartPoint.Y - PassedNode.Root.Y) + hypot(EndPoint.X - PassedNode.Interval.StartPoint.X, EndPoint.Y - PassedNode.Interval.StartPoint.Y) # Distance from Source-Root + Root-Point + Point-Target.
                elif IntersectionPoint.X > PassedNode.Interval.StartPoint.X and IntersectionPoint.X > PassedNode.Interval.EndPoint.X: # If the Root-EndPoint line travels to the right of the interval.
                    FValueEstimate = hypot(PassedNode.Root.X - StartPoint.X, PassedNode.Root.Y - StartPoint.Y) + hypot(PassedNode.Interval.EndPoint.X - PassedNode.Root.X, PassedNode.Interval.EndPoint.Y - PassedNode.Root.Y) + hypot(EndPoint.X - PassedNode.Interval.EndPoint.X, EndPoint.Y - PassedNode.Interval.EndPoint.Y) # Distance from Source-Root + Root-Point + Point-Target.
        return FValueEstimate

    def GenerateSuccessors(PassedNode):
        """
        Generates the successors of an Anya search node. Returns a tuple of the successor Nodes.
        """
        PrettyRoot = "{0}, {1}".format(PassedNode.Root.X, PassedNode.Root.Y)
        PrettyInterval = "{0}{1} --> {2}{3}".format("[" if PassedNode.Interval.StartFlag else "(", "(" + str(PassedNode.Interval.StartPoint.X) + ", " + str(PassedNode.Interval.StartPoint.Y) + ")", "(" + str(PassedNode.Interval.EndPoint.X) + ", " + str(PassedNode.Interval.EndPoint.Y) + ")", "]" if PassedNode.Interval.EndFlag else ")")
        Log("Anya: Generating succesors for node with root \"{0}\" and interval \"{1}\"".format(PrettyRoot, PrettyInterval), 0)
        def GenerateConeSuccessors(PointOne, PointTwo, Root):
            """
            Generates the successors of a cone search node.
            """
            global Node
            global Point
            NewInterval = None
            if PointOne.Y == PointTwo.Y == Root.Y: # If these are all on the same row (I.e. they are the non-observable successors of a flat node).
                NewRoot = FarthestPoint(Root, PointOne, PointTwo) # We have previously established that this is a turning point.
                print("NewRoot via FarthestPoint = {0}".format(NewRoot)) # TODO: TEMP
                Neighbors = GetGridData(PointOne.X, PointOne.Y, True) # We follow the edge of the obstacle to create the successor. The StartPoint for the new interval begins either directly above or below PointOne.
                if 1 in Neighbors[:2]: # We go up.
                    NewPointOne = Point(PointOne.X, PointOne.Y + 1)
                else: # We go down.
                    NewPointOne = Point(PointOne.X, PointOne.Y + 1)
                NewInterval = Interval(True, NewPointOne, Point(GridWidth, NewPointOne.Y), True)
            elif PointOne == PointTwo: # Non-observable successors of a cone node.
                NewRoot = PointOne
                if PointOne.Y - Root.Y > 0: # If the Root is below PointOne, we project the line upward.
                    NewPointOne = GetIntersectionPoint(Line(Root, PointOne), Line(Point(PointOne.X, PointOne.Y + 1), Point(PointTwo.X, PointTwo.Y + 1)), False)
                else: # The Root is above PointOne, so we project the line downward.
                    NewPointOne = GetIntersectionPoint(Line(Root, PointOne), Line(Point(PointOne.X, PointOne.Y - 1), Point(PointTwo.X, PointTwo.Y - 1)), False)
                NewInterval = Interval(True, NewPointOne, Point(GridWidth, NewPointOne.Y), True)
            else: # Observable successors of a cone node.
                NewRoot = Root
                if PointOne.Y - Root.Y > 0: # If the Root is below PointOne, we project the line upward.
                    NewPointOne = GetIntersectionPoint(Line(Root, PointOne), Line(Point(PointOne.X, PointOne.Y + 1), Point(PointTwo.X, PointTwo.Y + 1)), False)
                else: # The Root is above PointOne, so we project the line downward.
                    NewPointOne = GetIntersectionPoint(Line(Root, PointOne), Line(Point(PointOne.X, PointOne.Y - 1), Point(PointTwo.X, PointTwo.Y - 1)), False)
                if PointTwo.Y - Root.Y > 0: # If the Root is below PointTwo, we project the line upward.
                    NewPointTwo = GetIntersectionPoint(Line(Root, PointTwo), Line(Point(PointOne.X, PointOne.Y + 1), Point(PointTwo.X, PointTwo.Y + 1)), False)
                else: # The Root is above PointOne, so we project the line downward.
                    NewPointTwo = GetIntersectionPoint(Line(Root, PointTwo), Line(Point(PointOne.X, PointOne.Y - 1), Point(PointTwo.X, PointTwo.Y - 1)), False)
                NewInterval = Interval(True, NewPointOne, NewPointTwo, True)
            print("NewInterval is \"{0}\".".format(NewInterval)) # TODO: TEMP
            Successors = []
            for I in SplitInterval(NewInterval):
                NewNode = Node(I, NewRoot) # TODO: I don't get this... :/
                RenderAnya(GridData, None, [NewNode], None) # TODO: TEMP
                Successors = Successors.append(NewNode.Interval)
            print("ConeSuccessors are \"{0}\"".format(Successors)) # TODO: TEMP
            return Successors

        def GenerateFlatSuccessors(PointOne, Root):
            """
            Generates the successors of a flat search node.
            """
            PointTwo = GetFirstCornerPoint(PointOne)
            NewInterval = Interval(False, PointOne, PointTwo, True)
            Successors = []
            if Root.Y == PointOne.Y: # If these points are on the same row.
                Successors = GenerateSuccessors(Node(NewInterval, Root)) # Observable successors.
            else:
                Successors = GenerateSuccessors(Node(NewInterval, PointOne)) # Non-observable flat successors.
            print("FlatSuccessors are \"{0}\"".format(Successors)) # TODO: TEMP
            return Successors

        def GenerateStartSuccessors(StartPoint):
            """
            Generates the successors for the start search node.
            """
            global Node
            # Construct a maximal half-closed interval containing all points observable and to the left of StartPoint. (This does not include the StartPoint itself.)
            LeftStartInterval = []
            if LineOfSight(StartPoint, [0, StartPoint.Y]):
                LeftStartInterval = Interval(True, Point(0, StartPoint.Y), StartPoint, False)
            else:
                LeftPoints = BresenhamLinePoints(StartPoint, Point(0, StartPoint.Y))
                for PointIndex, LeftPoint in enumerate(LeftPoints):
                    if GetGridData(LeftPoint.X, LeftPoint.Y) == 1:
                        LeftStartInterval = Interval(True, LeftPoints[PointIndex], StartPoint, False)
            # Construct a maximal half-closed interval containing all points observable and to the right of StartPoint. (This does not include the StartPoint itself.)
            RightStartInterval = []
            if LineOfSight(StartPoint, Point(GridWidth, StartPoint.Y)):
                RightStartInterval = Interval(False, StartPoint, Point(GridWidth, StartPoint.Y))
            else:
                RightPoints = BresenhamLinePoints(StartPoint, Point(GridWidth, StartPoint.Y))
                for PointIndex, RightPoint in enumerate(RightPoints):
                    if GetGridData(RightPoint.X, RightPoint.Y) == 1:
                        RightStartInterval = Interval(False, StartPoint, RightPoints[PointIndex], True)
            # Construct a maximal half-closed interval containing all points observable and from the row above StartPoint.
            UpperLeftPoints = BresenhamLinePoints(Point(0, StartPoint.Y + 1), Point(StartPoint.X, StartPoint.Y + 1))
            UpperRightPoints = BresenhamLinePoints(Point(StartPoint.X, StartPoint.Y + 1), Point(GridWidth, StartPoint.Y + 1))
            if LineOfSight(StartPoint, Point(0, StartPoint.Y + 1)): # If there is a LOS from the Root to the leftmost point in the upper row.
                UpperStartIntervalLeft = [True, Point(0, StartPoint.Y + 1)]
            else: # Scan left until we no longer have a LOS.
                for PointIndex, LeftPoint in enumerate(UpperLeftPoints):
                    if not LineOfSight(StartPoint, LeftPoint):
                        UpperStartIntervalLeft = [True, UpperLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, Point(GridWidth, StartPoint.Y + 1)): # If there is a LOS from the Root to the rightmost point in the upper row.
                UpperStartIntervalRight = [Point(GridWidth, StartPoint.Y + 1), True]
            else: # Scan right until we no longer have a LOS.
                for PointIndex, RightPoint in enumerate(UpperRightPoints):
                    if not LineOfSight(StartPoint, RightPoint):
                        UpperStartIntervalRight = [UpperRightPoints[PointIndex - 1], True]
            UpperStartInterval = Interval(UpperStartIntervalLeft[0], UpperStartIntervalLeft[1], UpperStartIntervalRight[0], UpperStartIntervalRight[1])
            # Construct a maximal half-closed interval containing all points observable and from the row below StartPoint.
            LowerLeftPoints = BresenhamLinePoints(Point(0, StartPoint.Y - 1), Point(StartPoint.X, StartPoint.Y - 1))
            LowerRightPoints = BresenhamLinePoints(Point(StartPoint.X, StartPoint.Y - 1), Point(GridWidth, StartPoint.Y - 1))
            if LineOfSight(StartPoint, Point(0, StartPoint.Y - 1)): # If there is a LOS from the Root to the leftmost point in the lower row.
                LowerStartIntervalLeft = [True, Point(0, StartPoint.Y - 1)]
            else: # Scan left until we no longer have a LOS.
                for PointIndex, LeftPoint in enumerate(LowerLeftPoints):
                    if not LineOfSight(StartPoint, LeftPoint):
                        LowerStartIntervalLeft = [True, LowerLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, Point(GridWidth, StartPoint.Y - 1)):
                LowerStartIntervalRight = [Point(GridWidth, StartPoint.Y - 1), True]
            else: # Scan right until we no longer have a LOS.
                for PointIndex, RightPoint in enumerate(LowerRightPoints):
                    if not LineOfSight(StartPoint, RightPoint):
                        LowerStartIntervalRight = [LowerRightPoints[PointIndex - 1], True]
            LowerStartInterval = Interval(LowerStartIntervalLeft[0], LowerStartIntervalLeft[1], LowerStartIntervalRight[0], LowerStartIntervalRight[1])
            # Split each interval at any corner points.
            Intervals = set().union(SplitInterval(LeftStartInterval), SplitInterval(RightStartInterval), SplitInterval(UpperStartInterval), SplitInterval(LowerStartInterval))
            StartSuccessors = [GenerateSuccessors(Node(I, StartPoint)) for I in Intervals]
            print("StartSuccessors are \"{0}\"".format(StartSuccessors)) # TODO: TEMP
            return StartSuccessors

        Type = NodeType(PassedNode)
        if Type == "START":
            Successors = GenerateStartSuccessors(StartPoint)
        elif Type == "FLAT":
            FarPoint = FarthestPoint(PassedNode.Root, PassedNode.Interval.StartPoint, PassedNode.Interval.EndPoint)
            Successors = GenerateFlatSuccessors(FarPoint, PassedNode.Root) # The Point passed is the Point in the Interval which is farthest from the Node's Root. Only one successor should be created...
            if IsTurningPoint(PassedNode.Root, FarPoint):
                Successors.append(GenerateConeSuccessors(FarPoint, FarPoint, PassedNode.Root)) # These are non-observable successors.
        else: # Type == "CONE"
            Successors = GenerateConeSuccessors(PassedNode.Interval.StartPoint, PassedNode.Interval.EndPoint, PassedNode.Root) # Observable successors.
            if IsTurningPoint(PassedNode.Root, PassedNode.Interval.StartPoint):
                Successors.append(GenerateFlatSuccessors(PassedNode.Interval.StartPoint, PassedNode.Root)) # Non-observable successors.
                Successors.append(GenerateConeSuccessors(PassedNode.Interval.StartPoint, PassedNode.Interval.StartPoint, PassedNode.Root)) # More non-observable successors.
            if IsTurningPoint(PassedNode.Root, PassedNode.Interval.EndPoint):
                Successors.append(GenerateFlatSuccessors(PassedNode.Interval.EndPoint, PassedNode.Root)) # Non-observable successors.
                Successors.append(GenerateConeSuccessors(PassedNode.Interval.EndPoint, PassedNode.Interval.EndPoint, PassedNode.Root)) # More non-observable successors.
        Log("Anya: Successors for Root {0} created at {1}.".format(PassedNode.Root, Successors), 0)
        return Successors

    def GetFirstCornerPoint(PassedStartPoint):
        """
        Returns the first corner point in a row, moving right from the starting point. Otherwise returns the right-most point on the grid.
        """
        I = 0 # TODO: Find some nicer way of incrementing.
        MaximumXCoordinateValue = GridWidth + 1
        RowLength = ceil(MaximumXCoordinateValue - PassedStartPoint.X) # We add one ["!"] to GridWidth to account for the fact that there is a coordinate column AFTER the last square row.
        while I != RowLength: # From left to right, scan each point along the interval for a corner.
            Neighbors = Counter(GetGridData(PassedStartPoint.X + I, PassedStartPoint.Y, True))
            if Neighbors["0"] == 3 and Neighbors["1"] == 1: # We have found a corner point!
                return Point(PassedStartPoint.X + I, PassedStartPoint.Y) # Return the corner point.
            I += 1
        return Point(GridWidth + 1, PassedStartPoint.Y) # If we didn't find any corner points, return the right-most coordinate point. (We add one ["1"] because we are looking for the last coordinate, which lies after the last line in the grid.)

    def GetGridData(X, Y, GetNeighbors=False):
        """
        Provides an easy to determine the value of a specific coordinate square in the grid.
        Pass with "GetNeighbors=True" to get the value of the squares surrounding a specific coordinate.
        """
        # TODO: Place into documentation: Note that the coordinates run *between* the lines; so getting the value of "10, 10" would return the value of the square which occupies the space from 10,10 -> 11,11.
        # TODO: Place into documentation: "Round coordinates" (I.e. integers as opposed to floats) will return a list with the four nearest square values, while float coordinates will return either the nearest or two nearest square values.
        if GetNeighbors:
            if type(X) != int and type(Y) != int: # They are formatted as floating point numbers.
                if X.is_integer() and Y.is_integer(): # But still evaluate to integers.
                    X, Y = int(X), int(Y)
                    try:
                        QuadrantOne = GridData[Y][X]
                    except IndexError:
                        QuadrantOne = 0
                    try:
                        QuadrantTwo = GridData[Y][X-1]
                    except IndexError:
                        QuadrantTwo = 0
                    try:
                        QuadrantThree = GridData[Y - 1][X - 1]
                    except IndexError:
                        QuadrantThree = 0
                    try:
                        QuadrantFour = GridData[Y - 1][X]
                    except IndexError:
                        QuadrantFour = 0
                    return [QuadrantOne, QuadrantTwo, QuadrantThree, QuadrantFour]
                elif not X.is_integer() and Y.is_integer():
                    Y = int(Y)
                    try:
                        QuadrantsOneAndTwo = GridData[Y][floor(X)]
                    except IndexError:
                        QuadrantsOneAndTwo = 0
                    try:
                        QuadrantsThreeAndFour = GridData[Y - 1][floor(X)]
                    except IndexError:
                        QuadrantsThreeAndFour = 0
                    return [QuadrantsOneAndTwo, QuadrantsThreeAndFour]
                elif X.is_integer() and not Y.is_integer():
                    X = int(X)
                    try:
                        QuadrantsTwoAndThree = GridData[floor(Y)][X]
                    except IndexError:
                        QuadrantsTwoAndThree = 0
                    try:
                        QuadrantsFourAndOne = GridData[floor(Y)][X - 1]
                    except IndexError:
                        QuadrantsFourAndOne = 0
                    return [QuadrantsTwoAndThree, QuadrantsFourAndOne]
                # Both X and Y are floats.
                try:
                    QuadrantsAll = GridData[floor(Y)][floor(X)]
                except IndexError:
                    QuadrantsAll = 0
                return [QuadrantsAll]
            else: # They are allready integers (type=int).
                try:
                    QuadrantOne = GridData[Y][X]
                except IndexError:
                    QuadrantOne = 0
                try:
                    QuadrantTwo = GridData[Y][X-1]
                except IndexError:
                    QuadrantTwo = 0
                try:
                    QuadrantThree = GridData[Y - 1][X - 1]
                except IndexError:
                    QuadrantThree = 0
                try:
                    QuadrantFour = GridData[Y - 1][X]
                except IndexError:
                    QuadrantFour = 0
                return [QuadrantOne, QuadrantTwo, QuadrantThree, QuadrantFour]
        return GridData[Y - 1][X - 1]

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

    def IsTurningPoint(PreviousPoint, PassedPoint):
        """
        Determines if a point is a turning point.
        """
        Neighbors = Counter(GetGridData(PassedPoint.X, PassedPoint.Y, True))
        if Neighbors["0"] == 3 and Neighbors["1"] == 1: # The point lies on a corner.
            return True

    def LiesWithin(PassedPoint, PassedInterval): # TODO: Complete this function.
        """
        Determines whether a point lies within an interval.
        """
        if PassedPoint.Y == PassedInterval.StartPoint.Y == PassedInterval.EndPoint.Y and PassedInterval.StartPoint.X <= PassedPoint.X <= PassedInterval.EndPoint.X:
            return True

    def LineOfSight(PointOne, PointTwo):
        """
        Determines whether two points have a line-of-sight; that is, if a line drawn between them does not intersect with any solid (non-traversable) points.
        """
        LinePoints = BresenhamLinePoints(PointOne, PointTwo)
        if any(GetGridData(LinePoint.X, LinePoint.Y) for LinePoint in LinePoints) == 1:
            return False
        else:
            return True

    def NodeType(PassedNode):
        """
        Determines and returns the type of an Anya search PassedNode.
        """
        if PassedNode.Root == Point(-1, -1): # If the root of the PassedNode is off the map.
            return "START"
        elif PassedNode.Root.Y != PassedNode.Interval.StartPoint.Y and PassedNode.Root.Y != PassedNode.Interval.EndPoint.Y: # If the root of the PassedNode is not on the same line (does not have the same Y value) as the points contained in the Interval.
            return "CONE"
        elif PassedNode.Root.Y == PassedNode.Interval.StartPoint.Y and PassedNode.Root.Y == PassedNode.Interval.EndPoint.Y: # If the root of the PassedNode is on the same line as the (has the same Y value) as the points contained in the Interval.
            return "FLAT"

    def PathTo(PassedEndPoint):
        Log("Anya: Path found to EndPoint!", 0)

    def ProjectNode(PassedNode): # TODO: Complete this function.
        """
        Computes and returns the maximum observable interval projection for the node passed.
        If the projection is invalid, returns False.
        """
        if NodeType(PassedNode) == "FLAT":
            pass
        elif NodeType(PassedNode) == "CONE":
            if PassedNode.Interval.EndPoint.Y > PassedNode.Root.Y: # Project up, because the EndPoint is above the root.
                pass
            elif PassedNode.Interval.EndPoint.Y < PassedNode.Root.Y: # Project down, because the EndPoint is below the root.
                pass

    def ShouldPrune(PassedNode): # TODO: Complete this function.
        """
        Determines whether an Anya search Node should be pruned.
        """
        def IsCulDeSac(PassedNode):
            """
            Determines whether an Anya search Node is a "Cul De Sac".
            """
            ProjectedInterval = ProjectNode(PassedNode)
            if ProjectedInterval: # If the ProjectedInterval is valid.
                return False
        def IsIntermediate(PassedNode):
            """
            Determines whether an Anya search Node is an intermediate Node.
            """
            if NodeType(PassedNode) == "FLAT":
                FarPoint = None # TODO: Determine which Point in the Interval is farthest from the Node's Root.
                if IsTurningPoint(PassedNode.Root, PassedNode.Interval.StartPoint, FarPoint): # If FarPoint is a turning point for a taut local path with prefix (Root, Point), then the Node must have at least one non-observable successor; it cannot be intermediate.
                    return False
            else: # The Node is not a flat node; therefore it must be a cone node.
                if Interval: # TODO: "If Interval has a closed endpoint that is also a corner point..."
                    return False
                ProjectedInterval = ProjectNode(PassedNode)
                if ProjectedInterval: # TODO: "If ProjectedInterval contains any corner points..."
                    return False
            return True
        #IsCulDeSac(Node)
        #IsIntermediate(Node)
        return

    def SplitInterval(IntervalToBeSplit, ReturnUnsplitInterval=True):
        """
        Splits an Interval at any corner points into a new interval. Returns a tuple containing any new intervals. If no new intervals were created, returns False. (Call with "ReturnUnsplitInterval=False" to return False if the original interval was not split.)
        """
        Intervals = []
        I = 0 # TODO: Find some nicer way of incrementing.
        IntervalLength = ceil(IntervalToBeSplit.EndPoint.X - IntervalToBeSplit.StartPoint.X)
        while I != IntervalLength: # From left to right, scan each point along the interval for a corner.
            Neighbors = Counter(GetGridData(IntervalToBeSplit.StartPoint.X + I, IntervalToBeSplit.StartPoint.Y, True))
            if Neighbors["0"] == 3 and Neighbors["1"] == 1: # Create a new interval if we detect a corner point.
                Intervals.append(Interval(IntervalToBeSplit.StartFlag, IntervalToBeSplit.StartPoint, Point(IntervalToBeSplit.StartPoint.X + I, IntervalToBeSplit.EndPoint.Y), False))
                IntervalToBeSplit = Interval(False, IntervalToBeSplit.StartPoint.X + I, IntervalToBeSplit.EndPoint, True)
                IntervalLength = ceil(IntervalToBeSplit.EndPoint.X - IntervalToBeSplit.StartPoint.X) # Get the length of the remainder (latter half) of the original interval.
            I += 1
        if not Intervals and ReturnUnsplitInterval:
            return [IntervalToBeSplit]
        return Intervals

    #
    # Mainline function code.
    #

    StepPathData = []
    StartNode = Node(Interval(True, StartPoint, StartPoint, True), Point(-1, -1))
    Open = [StartNode]
    while Open:
        CurrentNode = Open.pop()
        if LiesWithin(EndPoint, CurrentNode.Interval):
            return PathTo(EndPoint)
        for SuccessorNode in GenerateSuccessors(CurrentNode):
            if not ShouldPrune(SuccessorNode):
                Open = Open | SuccessorNode
    return

  ####################################################
 #                                                  ##
#################################################### #
#                                                  # #
#                                                  # #
#                                                  # #
# TODO: Remove all below once testing is complete! # #
#                                                  # #
#                                                  # #
#                                                  ##
####################################################

#
# Temporary copied functions from Pathfinding.py.
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
        Coordinate = Point(Y, X) if IsSteep else Point(X, Y)
        Points.append(Coordinate)
        Error -= abs(DY)
        if Error < 0:
            Y += YStep
            Error += DX
    if Swapped:
        Points.reverse()
    return Points

def GetIntersectionPoint(LineOne, LineTwo, LineSegments=True):
    """
    Determines and returns the intersection point of two line segments.
    Returns False if the line segments do not intersect.
    Can be called with "LineSegments = False" to calculate the intersections of unbounded lines.
    """
    X1, Y1, X2, Y2, X3, Y3, X4, Y4 = LineOne.PointOne.X, LineOne.PointOne.Y, LineOne.PointTwo.X, LineOne.PointTwo.Y, LineTwo.PointOne.X, LineTwo.PointOne.Y, LineTwo.PointTwo.X, LineTwo.PointTwo.Y
    UaNumerator = ((X4 - X3) * (Y1 - Y3) - (Y4 - Y3) * (X1 - X3))
    UaDenominator = ((Y4 - Y3) * (X2 - X1) - (X4 - X3) * (Y2 - Y1))
    UbNumerator = ((X2 - X1) * (Y1 - Y3) - (Y2 - Y1) * (X1 - X3))
    UbDenominator = ((Y4 - Y3) * (X2 - X1) - (X4 - X3) * (Y2 - Y1))
    if UaNumerator == 0 and UaDenominator == 0 and UaNumerator == 0 and UbDenominator == 0: # If the lines are coincident.
        return
    elif UaDenominator == 0 and UbDenominator == 0: # If the lines are parallel.
        return
    else:
        Ua = UaNumerator / UaDenominator
        Ub = UbNumerator / UbDenominator
        X = X1 + Ua * (X2 - X1)
        Y = Y1 + Ua * (Y2 - Y1)
        IntersectionPoint = Point(X, Y)
        if not LineSegments: # If they are lines.
            return IntersectionPoint
        elif 0 <= Ua <= 1 and 0 <= Ub <= 1: # If they are line segments and they intersect:
            return IntersectionPoint

#
# Temporary Mainline code.
#

#MapFile = input("Please enter map file name: ")
#Sx = input("Please enter X pos. of StartPoint: ")
#Sy = input("Please enter Y pos. of StartPoint: ")
#Ex = input("Please enter X pos. of EndPoint: ")
#Ey = input("Please enter Y pos. of EndPoint: ")
#StartPoint = [Sx, Sy]
#EndPoint = [Ex, Ey]

MapFile = "test3.map"
TupleStartPoint = [175, 35]
TupleEndPoint = [1000, 875]

GridData = []

with open(MapFile, "r") as File:
    GridData = File.readlines()[::-1] # We reverse and make a shallow copy of the list.

GridData = [list(Line.strip()) for Line in GridData] # Remove newlines.
for RowIndex, Row in enumerate(GridData):
    for CharacterIndex, Character in enumerate(GridData[RowIndex]):
        GridData[RowIndex][CharacterIndex] = int(Character) # Split each line character-by-character, and convert each character from a string into an integer.

print("Map loaded! Filename: \"{0}\". Map dimensions: {1} * {2}.".format(MapFile, len(GridData[0]), len(GridData)))
RenderAnya(GridData, "_AnyaRender GridData")

StartTime = time.time()
StepPathData = Anya(GridData, TupleStartPoint, TupleEndPoint)
EndTime = time.time()
RunTime = EndTime - StartTime

print("Anya complete! Estimated run time: {0}.".format(RunTime))
