# -*- coding: utf8 *-*

#
# Built-in imports.
#

from collections import namedtuple
import sys

#
# Custom imports.
#

from RenderAnya import RenderAnya # TODO: Change this into the proper Render import once testing on Anya is completed.

#
# Functions.
#

def Anya(GridData, StartPoint, EndPoint):
    """
    Find the optimal path between two points on a grid. Returns tuple with each point in the path. Returns False if no path exists.
    Anya implementation based on the paper "Optimal Any-angle Pathfinding in Practice", published in the Journal of Artificial Intelligence Research (JAIR); written by D. Harabor, A. Grastien, D. Öz and V. Aksakalli; 2016.
    """
    #
    # Function variables.
    #

    GridHeight = len(GridData) - 1
    GridWidth = len(GridData[0]) - 1
    Interval = namedtuple("Interval", "StartFlag StartPoint EndPoint EndFlag")
    Node = namedtuple("Node", "Interval Root")
    Point = namedtuple("Point", "X Y")
    # Complete set-up of variables "Interval", "Node", and "Point".
    Interval.StartFlag = True
    Interval.StartPoint = Point
    Interval.EndPoint = Point
    Interval.EndFlag = True
    Node.Interval = Interval
    Node.Root = Point
    # Back to regular variables.
    RootHistory = []

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
            pass

        def GenerateStartSuccessors(StartPoint):
            """
            Generates the successors for the start search node.
            """
            # Construct a maximal half-closed interval containing all points observable and to the left of StartPoint. (This does not include the StartPoint itself.)
            LeftStartInterval = []
            if LineOfSight(StartPoint, [0, StartPoint[1]]):
                LeftStartInterval = [True, [0, StartPoint[1]], StartPoint, False]
            else:
                LeftPoints = BresenhamLinePoints(StartPoint, [0, StartPoint[1]])
                for Point, PointIndex in enumerate(LeftPoints):
                    if GridData[Point[1]][Point[0]] == 1:
                        LeftStartInterval = [True, LeftPoints[PointIndex], StartPoint, False]
            # Construct a maximal half-closed interval containing all points observable and to the right of StartPoint. (This does not include the StartPoint itself.)
            RightPoints = BresenhamLinePoints(StartPoint, [GridWidth, StartPoint[1]])
            RightStartInterval = []
            if LineOfSight(StartPoint, [GridWidth, StartPoint[1]]):
                RightStartInterval = [False, StartPoint, [GridWidth, StartPoint[1]], True]
            else:
                RightPoints = BresenhamLinePoints(StartPoint, [GridWidth, StartPoint[1]])
                for Point, PointIndex in enumerate(RightPoints):
                    if GridData[Point[1]][Point[0]] == 1:
                        RightStartInterval = [False, StartPoint, RightPoints[PointIndex], True]
            # Construct a maximal half-closed interval containing all points observable and from the row above StartPoint.
            UpperLeftPoints = BresenhamLinePoints([0, StartPoint[1] + 1], [StartPoint[0], StartPoint[1] + 1])
            UpperRightPoints = BresenhamLinePoints([[StartPoint[0], StartPoint[1] + 1]], [GridWidth, StartPoint[1] + 1])
            if LineOfSight(StartPoint, [0, StartPoint[1]]): # If there is a LOS from the Root to the leftmost point in the upper row.
                UpperStartIntervalLeft = [True, [0, StartPoint[1] + 1]]
            else: # Move left until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperLeftPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalLeft = [True, UpperLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, [GridWidth, StartPoint[1] + 1]): # If there is a LOS from the Root to the rightmost point in the upper row.
                UpperStartIntervalRight = [[GridWidth, StartPoint[1] + 1], True]
            else: # Move right until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperRightPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalRight = [UpperRightPoints[PointIndex - 1], True]
            UpperStartInterval = UpperStartIntervalLeft + UpperStartIntervalRight
            # Construct a maximal half-closed interval containing all points observable and from the row below StartPoint.
            LowerLeftPoints = BresenhamLinePoints([0, StartPoint[1] - 1], [StartPoint[0], StartPoint[1] - 1])
            UpperRightPoints = BresenhamLinePoints(StartPoint, [GridWidth, StartPoint[1] + 1])
            if LineOfSight(StartPoint, [0, StartPoint[1]]): # If there is a LOS from the Root to the leftmost point in the lower row.
                UpperStartIntervalLeft = [True, [0, StartPoint[1] + 1]]
            else: # Move left until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperLeftPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalLeft = [True, UpperLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, [GridWidth, StartPoint[1] + 1]): # If there is a LOS from the Root to the rightmost point in the lower row.
                UpperStartIntervalRight = [[GridWidth, StartPoint[1] + 1], True]
            else: # Move right until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperRightPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalRight = [UpperRightPoints[PointIndex - 1], True]
            UpperStartInterval = UpperStartIntervalLeft + UpperStartIntervalRight
            # Split each interval at any corner points.
            Intervals = [SplitInterval(LeftStartInterval), SplitInterval(RightStartInterval), SplitInterval(UpperStartInterval), SplitInterval(LowerStartInterval)]
            Log("Anya Intervals for Root {0} created at {1}".format(Root, Intervals), 0)
            Root = StartPoint # The root for all of the StartSuccessors is the StartPoint.
            StartSuccessors = [GenerateSuccessors((Root, Interval)) for Interval in Intervals]
            return StartSuccessors

    StepPathData = []
    return StepPathData

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
StartPoint = [95, 10]
EndPoint = [5, 30]

GridData = []

with open(MapFile, "r") as File:
    GridData = File.readlines()[::-1] # We reverse the list.

GridData = [list(Line.strip()) for Line in GridData]
for LineIndex, Line in enumerate(GridData):
    for CharacterIndex, Character in enumerate(GridData[LineIndex]):
        GridData[LineIndex][CharacterIndex] = int(Character)

print("Map loaded! Filename: \"{0}\". Map dimensions: {1} * {2}.".format(MapFile, len(GridData[0]), len(GridData)))
#print("Raw map data:\r\n{0}".format(GridData))
RenderAnya(GridData)


StepPathData = Anya(GridData, StartPoint, EndPoint)

print("Anya complete!")