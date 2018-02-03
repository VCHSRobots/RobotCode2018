# Line Intersection Benchmarking

#
# Built-in imports.
#

from timeit import timeit

#
# Custom imports.
#

from Pathfinding import GetIntersectionPoint
from simulatelidar import IntersectPoints

#
# Functions.
#

#
# Mainline code.
#

print("Temporary Line Intersection Method Benchmarking!")

print("Method 1: Pathfinding.GetIntersectionPoint()")
Time1 = timeit("GetIntersectionPoint(((2, 4), (12, 10)), ((4, 8), (14, 4)))", "from Pathfinding import GetIntersectionPoint", number = 1000000)
print("Time to run 1,000,000 times: {0} seconds.".format(Time1))
print("Method 2: simulatelidar")
Time2 = timeit("IntersectPoints(((2, 4), (12, 10)), ((4, 8), (14, 4)))", "from simulatelidar import IntersectPoints", number = 1000000)
print("Time to run 1,000,000 times: {0} seconds.".format(Time2))
Difference = round(((Time2 - Time1) / Time2) * 100)
print("Percent difference in speed: Method 1 is {0}% faster then method 2.".format(Difference))