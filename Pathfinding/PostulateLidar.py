# PostulateLidar.py: Tests Patrick's positioning algorithm
# 1-6-2018
#
import json
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        x = (self.x - point.x) ** 2
        y = (self.y - point.y) ** 2
        return (x + y) ** .5

    def isInQuadrant(self, origin):
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


class Line:

    def yInter(self):
        inter = (-self.slope * self.p1.x) + self.p1.y
        return inter

    def findSlope(self, p1, p2):
        xdif = p1.x - p2.x
        if xdif == 0:
            slope = None
        else:
            slope = (p1.y - p2.y) / (p1.x - p2.x)
        return slope

    def findXWithY(self, y):
        x = y - self.inter
        return x

    def findYWithX(self, x):
        y = (self.slope * x) + self.inter
        return y


class LineSeg(Line):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = self.findSlope(p1, p2)
        if self.slope is not None:
            self.inter = self.yInter()
            self.ang = rad2deg(np.arctan(self.slope / 1))
        else:
            self.inter = None
            self.x = self.p1.x
            self.ang = 90
        self.point = self.p1

    def isReal(self, point):
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
            return False
        else:
            return True

    def solveXInter(self, obj):
        """Solves for the x inercept between two lines in slope"""
        if self.slope is None or obj.slope is None:
            return False
        v = self.slope - obj.slope
        c = obj.inter - self.inter
        if v == 0:
            if c:
                c = None
            else:
                c = 0
        else:
            c /= v
        return c

    def findinter(self, obj):
        x = self.solveXInter(obj)
        if x is None:
            return None
        elif x is False:
            if self.slope is None:
                objs = [self, obj]
            else:
                objs = [obj, self]
            x = objs[0].x
            if type(x) == int or type(x) == float:
                y = objs[1].findYWithX(x)
            else:
                return None
        else:
            y = (self.slope * x) + self.inter
        point = Point(x, y)
        if self.isReal(point) and obj.isReal(point):
            return point


class Ray(Line):
    def __init__(self, ang, point):
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

    def isReal(self, point):
        pointquad = point.isInQuadrant(self.point)
        if self.quadrant == pointquad: # or (self.quadrant - pointquad)%2 != 0:
            return True
        else:
            return False


def rad2deg(rad):
    pi = 3.1415926535897932384626433832
    deg = rad * (180 / pi)
    return deg


def deg2rad(deg):
    pi = 3.1415926535897932384626433832
    rad = deg / (180 / pi)
    return rad


def angledRayIntersects(robotlocation, robotangle, samplerate = 1, debug = False):
    rayinters = {}
    debuginters = []
    fieldlines = openEnvFile("FRC_Field_2018.map")
    ang = 0
    while ang < 360:
        i = findLineIntersects(ang, robotlocation, fieldlines)
        if i:
            if debug:
                debuginters.append(i)
            rayinters[ang] = robotlocation.dist(i)
        ang += samplerate
    rayinters = compForAngle(rayinters, robotangle)
    if debug:
        writeFieldSvg(robotlocation, debuginters, fn="2018FRC.svg", lines=fieldlines)
    # outputJsonOfInters(rayinters, robotlocation)
    return rayinters


def compForAngle(rayinters, robotangle):
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

def findLineIntersects(ang, location, fieldlines):
    inters = []
    ray = Ray(ang, location)
    for line in fieldlines:
        inters.append(line.findinter(ray))
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
        dists[location.dist(point)] = point
    return dists


def filterNone(filtered):
    res = []
    for item in filtered:
        if item is not None:
            res.append(item)
    return res


def openEnvFile(env):
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


def writeFieldSvg(location, scans, fn, lines):
    fieldsgv = open(fn, "w")
    fieldsgv.write("""<!DOCTYPE html>
              <html>
              <body>
              """)
    fieldsgv.write('<svg height = "{0}" width = "{1}">\n'.format(648, 500))

    for line in lines:
        fieldsgv.write('<line x1 = "{0}" y1 = "{1}" '
                        'x2 = "{2}" y2 = "{3}" '
                        'style = "stroke:rgb(255,0,0);'
                        'stroke-width:2"/>\n'.format(
                        line.p1.x, line.p1.y, line.p2.x, line.p2.y))
    for inter in scans:
        fieldsgv.write('<line x1 = "{0}" y1 = "{1}" '
                        'x2 = "{2}" y2 = "{3}" '
                        'style = "stroke:rgb(255,255,0);'
                        'stroke-width:2"/>\n'.format(round(location.x), round(location.y),
                        round(inter.x), round(inter.y)))
    fieldsgv.write('<circle cx = "{0}" cy = "{1}" r = "10" '
                'stroke = "black" stroke-width = "3" fill = "yellow"/>\n'.format(location.x, location.y))
    fieldsgv.write("""<\svg>
             <\\body>
             <\html>""")
    fieldsgv.close()


def main():
    angledRayIntersects(Point(250, 350), 0, 1, debug = False)

def IntersectPoints(LineOne, LineTwo):
    seg1 = LineSeg(Point(LineOne[0][0], LineOne[0][1]), Point(LineOne[1][0], LineOne[1][1]))
    seg2 = LineSeg(Point(LineTwo[0][0], LineOne[0][1]), Point(LineTwo[1][0], LineTwo[1][1]))
    inter = seg1.findinter(seg2)
    return inter

# main()
