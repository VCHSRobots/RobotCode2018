# simulatelidar.py: Tests Patrick's positioning algorithm
# 1-6-2018
#
import json
import numpy as np

cdef class Point:

    cdef public float x, y

    def __cinit__(self, x, y):
        self.x = x
        self.y = y


"""
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        x = (self.x - point.x) ** 2
        y = (self.y - point.y) ** 2
        return (x + y) ** .5
"""

cdef int isInQuadrant(Point self, Point origin):
    if self.y == origin.y:
        if self.x > origin.x:
            return 1
        elif self.x < origin.x:
            return 3
    elif self.x > origin.x:
        if self.y >= origin.y:
            return 1
        else:
            return 4
    elif self.x < origin.x:
        if self.y >= origin.y:
            return 2
        else:
            return 3
    elif self.x == origin.x:
        if self.y > origin.y:
            return 2
        elif self.y < origin.y:
            return 4


cdef double yInter(self):
    inter = (-self.slope * self.p1.x) + self.p1.y
    return inter

def findSlope(self, p1, p2):
    xdif = p1.x - p2.x
    if xdif == 0:
        slope = None
    else:
        slope = (p1.y - p2.y) / (p1.x - p2.x)
    return slope

cdef float findXWithY(self, y):
    x = y - self.inter
    return x

cdef float findYWithX(self, x):
    y = (self.slope * x) + self.inter
    return y


class LineSeg:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = findSlope(self, p1, p2)
        if self.slope is not None:
            self.inter = yInter(self)
            self.ang = rad2deg(np.arctan(self.slope / 1))
        else:
            self.inter = None
            self.x = self.p1.x
            self.ang = 90
        self.point = self.p1

cdef int segIsReal(self, point):
    if self.p1.x > self.p2.x:
        maxx = self.p1.x
        minx = self.p2.x
    else:
        minx = self.p1.x
        maxx = self.p2.x
    if self.p1.y > self.p2.y:
        maxy = self.p1.y
        miny = self.p2.y
    else:
        miny = self.p1.y
        maxy = self.p2.y
    if point.x > maxx or point.x < minx or point.y > maxy or point.y < miny:
        return 0
    else:
        return 1


def solveXInter(self, obj):
    """Solves for the x intercept between two lines in slope"""
    v = self.slope - obj.slope
    c = obj.inter - self.inter
    c /= v
    return c


cdef Point findValidInter(self, obj):
    x = solveXInter(self, obj)
    y = (self.slope * x) + self.inter
    point = Point(x, y)
    return point


def findinter(self, obj):
    if self.slope is None or obj.slope is None:
        if self.slope is None:
            objs = [self, obj]
        else:
            objs = [obj, self]
        x = objs[0].x
        if type(x) == int or type(x) == float:
            y = findYWithX(objs[1], x)
            point = Point(x, y)
        else:
            return None
    elif self.slope == obj.slope:
        return None
    else:
        point = findValidInter(self, obj)
    if segIsReal(self, point) and rayIsReal(obj, point):
        return point


class Ray:
    def __init__(self, float ang, Point point):
        self.ang = ang
        self.point = point
        self.quadrant = int(self.ang / 90) + 1
        if self.quadrant == 2 or self.quadrant == 4:
            slopeang = 90 - (self.ang % 90)
        else:
            slopeang = self.ang % 90
        self.slope = round(np.tan(deg2rad(slopeang)), 5)
        if self.quadrant == 2 or self.quadrant == 4:
            self.slope *= -1
        if self.slope == 0:
            self.inter = self.point.y
            self.x = self.point.x
        else:
            self.inter = (-self.slope * self.point.x) + self.point.y

cdef int rayIsReal(self, point):
    pointquad = isInQuadrant(point, self.point)
    if self.quadrant == pointquad: # or (self.quadrant - pointquad)%2 != 0:
        return 1
    else:
        return 0


cdef double rad2deg(double rad):
    pi = 3.1415926535897932384626433832
    deg = rad * (180 / pi)
    return deg

#-
cdef double deg2rad(double deg):
    pi = 3.1415926535897932384626433832
    rad = deg / (180 / pi)
    return rad


cdef double dist(p1, p2):
    x = (p1.x - p2.x) ** 2
    y = (p1.y - p2.y) ** 2
    return (x + y) ** .5

# Function that needs the most optimizing
def angledRayIntersects(robotlocation, robotangle, samplerate = 1, debug = False):
    rayinters = {}
    debuginters = []
    fieldlines = openEnvFile("FRC_Field_2018.map")
    cdef int ang = 0
    while ang < 360:
        i = findLineIntersects(ang, robotlocation, fieldlines)
        if i:
            rayinters[ang] = dist(robotlocation, i)
        ang += samplerate
    rayinters = compForAngle(rayinters, robotangle)
    return rayinters


def compForAngle(rayinters, float robotangle):
    angles = []
    inters = []
    adjustedinters = {}
    for angle in rayinters:
        angles.append(angle)
        inters.append(rayinters[angle])
    for ind, angle in enumerate(angles):
        angles[ind] = (angles[ind] + robotangle) % 360
    for ind, angle in enumerate(angles):
        adjustedinters[angle] = inters[ind]
    return adjustedinters

def outputJsonOfInters(rayinters, location):
    lidarsim = open("lidarsim.json", "w")
    json.dump({
        "Name": "Lidar Simulation",
        "Location": [location.x, location.y],
        "Distances": rayinters
    }, lidarsim, indent = 2)

cdef Point findLineIntersects(float ang, Point location, fieldlines):
    inters = []
    ray = Ray(ang, location)
    for line in fieldlines:
        inters.append(findinter(line, ray))
    inters = filterNone(inters)
    dists = makeDictOfDists(inters, location)
    # try:
    closestpoint = sorted(dists)[0]
    return dists[closestpoint]
    # except IndexError:
    #     return None


def makeDictOfDists(inters, location):
    dists = {}
    for point in inters:
        dists[dist(location, point)] = point
    return dists


cdef list filterNone(filtered):
    res = []
    for item in filtered:
        if item is not None:
            res.append(item)
    return res


cdef list openEnvFile(env):
    lines = []
    file = open(env, "r")
    field = json.load(file)
    file.close()
    elements = field["Elements"]
    for e in elements:
        if elements[e]["Solidity"]:
            for l in findLinesFromPoints(elements[e]["Points"]):
                lines += [LineSeg(Point(l[0][0], l[0][1]), Point(l[1][0], l[1][1]))]
    return lines


def findLinesFromPoints(points):
    ret = []
    for ind, point in enumerate(points[:-1]):
        pair = [points[ind], points[ind + 1]]
        ret.append(pair)
    return ret


def main():
    angledRayIntersects(Point(250, 350), 0, 1, debug = False)


# main()
