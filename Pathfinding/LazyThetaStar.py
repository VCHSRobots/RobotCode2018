import heapq
import math
import time

#
# Classes.
#

class PriorityQueue():
    """
    An object heap.
    """
    def __init__(self):
        self.Elements = []

    def Insert(Point, GValue):
        """
        Inserts the passed item into Open, with it's passed GValue.
        """
        heapq.heappush(self.Elements, (GValue, Point))

    def Pop():
        """
        Pop in this context returns the point with the smallest GValue from Open.
        """
        return heapq.heappop(self.Elements)

    def Remove(Point): # TODO: Complete remove operation.
        """
        Removes (deletes) the passed item from Open.
        """
        pass

class Point():
    """
    The basic Point object.
    """
    def __init__(self, X, Y):
        """
        Initialize a new Point.
        """
        self.VisibleNeighbors = [NeighborPoint for NeighborPoint in [[X + 1, Y + 1], [X, Y + 1], [X - 1, Y + 1], [X - 1, Y], [X - 1, Y - 1], [X, Y - 1], [X + 1, Y - 1], [X + 1, Y]] if LineOfSight((self.X, self.Y), NeighborPoint)]
        self.X = X
        self.Y = Y
        self.Parent = None
        self.GValue = 0

#
# Functions.
#

def Main(StartPoint, EndPoint):
    StartPoint = Point(StartPoint[0], StartPoint[1])
    EndPoint = Point(EndPoint[0], EndPoint[1])
    Open = PriorityQueue()
    StartPoint.GValue = 0
    StartPoint.Parent = StartPoint
    Open[StartPoint] = StartPoint.GValue
    while Open:
        CurrentPoint = Open.Pop()
        print("CurrentPoint: {0}".format(CurrentPoint)) # TODO: TEMP
        if CurrentPoint.X == EndPoint.X and CurrentPoint.Y == EndPoint.Y:
            return "Path found!"
        Closed = list(set(Closed) | set([CurrentPoint.X, CurrentPoint.Y]))
        for Neighbor in CurrentPoint.VisibleNeighbors:
            if [Neighbor.X, Neighbor.Y] not in Closed:
                if [Neighbor.X, Neighbor.Y] not in Open:
                    

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
