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


cdef findSlope(self, p1, p2):
    xdif = p1.x - p2.x
    if xdif == 0:
        slope = None
    else:
        slope = (p1.y - p2.y) / (p1.x - p2.x)
    return slope

cdef float findXWithY(self, y):
    x = (y - self.inter)/self.slope
    return x

cdef float findYWithX(self, x):
    y = (self.slope * x) + self.inter
    return y


class LineSeg:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = findSlope(self, p1, p2)
        if self.slope is None:
            self.inter = None
            self.x = self.p1.x
            self.ang = 90
        else:
            self.inter = (-self.slope * self.p1.x) + self.p1.y
            self.ang = rad2deg(np.arctan(self.slope / 1))


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


cdef findinter(self, obj):
    X1, Y1, X2, Y2, X3, Y3, X4, Y4 = self.p1.x, self.p1.y, self.p2.x, self.p2.y, obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y
    UaNumerator = ((X4 - X3) * (Y1 - Y3) - (Y4 - Y3) * (X1 - X3))
    UaDenominator = ((Y4 - Y3) * (X2 - X1) - (X4 - X3) * (Y2 - Y1))
    UbNumerator = ((X2 - X1) * (Y1 - Y3) - (Y2 - Y1) * (X1 - X3))
    UbDenominator = ((Y4 - Y3) * (X2 - X1) - (X4 - X3) * (Y2 - Y1))
    if UaNumerator == 0 and UaDenominator == 0 and UbNumerator == 0 and UbDenominator == 0:  # If the lines are coincident.
        return None
    elif UaDenominator == 0 and UbDenominator == 0:  # If the lines are parallel.
        return None
    else:
        Ua = UaNumerator / UaDenominator
        Ub = UbNumerator / UbDenominator
        X = X1 + Ua * (X2 - X1)
        Y = Y1 + Ua * (Y2 - Y1)
        point = Point(X, Y)
        # if Ua > 0 and Ua < 1 and rayIsReal(obj, point):
        # if segIsReal(self, point) and rayIsReal(obj, point):
        if 0 <= Ua <= 1 and 0 <= Ub <= 1:
            return point


class Ray:
    def __init__(self, float ang, Point point):
        self.ang = ang
        self.p1 = point
        self.quadrant = int(self.ang / 90) + 1
        if self.quadrant == 2 or self.quadrant == 4:
            slopeang = 90 - (self.ang % 90)
        else:
            slopeang = self.ang % 90
        self.slope = round(np.tan(deg2rad(slopeang)), 3)
        if self.quadrant == 2 or self.quadrant == 4:
            self.slope *= -1
        if self.slope == 0:
            self.inter = self.p1.y
            self.x = self.p1.x
        else:
            self.inter = (-self.slope * self.p1.x) + self.p1.y
        if self.quadrant is 1 or self.quadrant is 4:
            self.p2 = Point(point.x + 500, point.y + (500 * self.slope))
        else:
            self.p2 = Point(point.x - 500, point.y - (500 * self.slope))


cdef int rayIsReal(self, point):
    pointquad = isInQuadrant(point, self.p1)
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
cpdef angledRayIntersects(Point robotlocation, robotangle, fieldlines, samplerate = 1):
    rayinters = []
    cdef int ang = 0
    while ang < 360:
        i = findLineIntersect(ang, robotlocation, fieldlines)
        if i:
            rayinters.append(dist(robotlocation, i))
        ang += samplerate
    # rayinters = compForAngle(rayinters, robotangle)
    return rayinters

cpdef dict customRayIntersects(Point robotlocation, list anglestopost, list fieldlines):
    cdef dict rayinters = {}
    for angle in anglestopost:
        intersect = findLineIntersect(angle, robotlocation, fieldlines)
        rayinters[angle] =  dist(robotlocation, intersect)
    return rayinters

cpdef Point pointFromDistAng(startpoint, ang, dist):
    quadrant = int(ang / 90) + 1
    x = dist * np.cos(deg2rad(ang))
    y = dist * np.sin(deg2rad(ang))
    distpoint = Point(startpoint.x + x ,startpoint.y + y)
    return distpoint


cdef compForAngle(rayinters, float robotangle):
    cdef list angles = []
    cdef list inters = []
    cdef dict adjustedinters = {}
    for angle in rayinters:
        angles.append(angle)
        inters.append(rayinters[angle])
    for ind, angle in enumerate(angles):
        angles[ind] = (angles[ind] + robotangle) % 360
    for ind, angle in enumerate(angles):
        adjustedinters[angle] = inters[ind]
    return adjustedinters


cdef Point findLineIntersect(float ang, Point location, list fieldlines):
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


cdef dict makeDictOfDists(inters, Point location):
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


cpdef list openEnvFile(env):
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


cdef list findLinesFromPoints(points):
    ret = []
    for ind, point in enumerate(points[:-1]):
        pair = [points[ind], points[ind + 1]]
        ret.append(pair)
    return ret
