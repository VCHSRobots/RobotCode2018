# DotCompare.py: Outputs difference between ideal and actual lidar data
# 1-18-2018

import numpy as np
import cProfile
import time
import json

###
import CythonLidarPost
import SweepCommunication


size = [324, 360]


def catchMyDrift(lidarid, location):
    # lidardists = parseLidar("COM3")
    fieldlines = CythonLidarPost.openEnvFile("FRC_Field_2018.map")
    lidardists = CythonLidarPost.customRayIntersects(CythonLidarPost.Point(location.x+1, location.x+1), list(range(1, 200)), fieldlines)
    location, ang, distdifs = findRobotLocation(lidardists, location, 15, 5, 15, fieldlines)
    print(location.x, location.y)
    obstacles = measureObstacles(distdifs, 6)
    obstaclepoints = extractPointsFromObstacles(obstacles, location, lidardists)
    return location, ang, obstaclepoints


def extractPointsFromObstacles(obstacles, location, lidardists):
    points = []
    for obstacle in obstacles:
        points.append([])
        for ang in obstacle:
            points[-1].append(CythonLidarPost.pointFromDistAng(location, ang, lidardists[ang]))
    return points


def measureObstacles(distdifs, sensitivity = 1):
    obstacle = 0
    obstacles = []
    for ang in distdifs:
        distdif = distdifs[ang]
        if distdif >= sensitivity: 
            obstacle += 1
        else:
            obstacle = 0
        if obstacle:
            if obstacle == 1:
                obstacles.append([ang])
            else:
                obstacles[-1].append(ang)
    return obstacles


def parseLidar(sweepusb):
    sweep = SweepCommunication.makeSweep(sweepusb)
    scans = SweepCommunication.scanRotation(sweep)
    return scans


# Depreciated
def findBestLocation(lidardists, location, testingrange, angoffsetrange):
    difvsret = {}
    # xs = tuple(range(location[0] - testingrange, location[0] + (testingrange + 1)))
    # ys = tuple(range(location[1] - testingrange, location[1] + (testingrange + 1)))
    # angs = tuple(range(location[2] - angoffsetrange, location[2] + angoffsetrange + 1))
    cordrange = np.array([[location[0] - testingrange, location[0] + testingrange],
                          [location[1] - testingrange, location[1] + testingrange]])
    cordrange[cordrange <= 0] = 1
    cordx = cordrange[0]
    cordy = cordrange[1]
    cordx[cordx >= size[0]] = size[0] - 1
    cordy[cordy >= size[1]] = size[1] - 1
    cordrange = np.array([cordx[0], cordx[1], cordy[0], cordy[1]])
    xs = tuple(range(cordrange[0], cordrange[1] + 1))
    ys = tuple(range(cordrange[2], cordrange[3] + 1))
    angs = tuple(range(location[2] - angoffsetrange, location[2] + angoffsetrange + 1))
    fieldlines = CythonLidarPost.openEnvFile("FRC_Field_2018.map")
    for x in xs:
        for y in ys:
            postdata = CythonLidarPost.customRayIntersects(CythonLidarPost.Point(x, y), 0, fieldlines)
            for angle in angs:
                idealdists = shiftInds(postdata, angle)
                difvsret[findDotDif(lidardists, idealdists)] = [(x, y), angle]
    bestdotdif = difvsret[sorted(difvsret)[0]]
    reallocation = [bestdotdif[0]]
    ang = bestdotdif[1]
    return (reallocation, ang), difvsret


def findRobotLocation(lidardists, location, angle, testingrange, angoffsetrange, fieldlines):
    difvsret = {}
    # xs = tuple(range(location[0] - testingrange, location[0] + (testingrange + 1)))
    # ys = tuple(range(location[1] - testingrange, location[1] + (testingrange + 1)))
    # angs = tuple(range(location[2] - angoffsetrange, location[2] + angoffsetrange + 1))
    cordrange = np.array([[location.x - testingrange, location.x + testingrange],
                          [location.y - testingrange, location.y + testingrange]])
    cordrange[cordrange <= 0] = 1
    cordx = cordrange[0]
    cordy = cordrange[1]
    cordx[cordx >= size[0]] = size[0] - 1
    cordy[cordy >= size[1]] = size[1] - 1
    cordrange = np.array([cordx[0], cordx[1], cordy[0], cordy[1]])
    xs = tuple(range(int(cordrange[0]), int(cordrange[1] + 1)))
    ys = tuple(range(int(cordrange[2]), int(cordrange[3] + 1)))
    angs = tuple(range(angle - angoffsetrange, angle + angoffsetrange + 1))
    lidardists = CmToInchesInDict(lidardists)
    lidarkeys = list(lidardists.keys())
    for x in xs:
        for y in ys:
            postdata = CythonLidarPost.customRayIntersects(CythonLidarPost.Point(x, y), lidarkeys, fieldlines)
            for angle in angs:
                idealdists = shiftKeys(postdata, angle)
                # distdifs = findDistDifs(lidardists, idealdists)
                # lidardists = accountForObstacles(lidardists, measureObstacles(distdifs, sensitivity = 20))
                difvsret[findDotDif(lidardists, idealdists)] = [CythonLidarPost.Point(x, y), angle, idealdists]
    bestdotdif = difvsret[sorted(difvsret)[0]]
    location = bestdotdif[0]
    angle = bestdotdif[1]
    distdifs = (findDistDifs(lidardists, bestdotdif[2]))
    return location, angle, distdifs


def CmToInchesInDict(dict):
    inchDict = {}
    dictvalues = np.array(list(dict.values()))
    dictvalues *= .3937088
    for ind, key in enumerate(dict):
        inchDict[key] = dictvalues[ind]
    print(inchDict)
    return inchDict


"""
def findBestLocation(lidardists, location, testingrange, angoffsetrange):
    ang = findClosestDot(lidardists, angoffsetrange[0], angoffsetrange[1], "angle", location = location)
    location = findClosestDot(lidardists, -testingrange, testingrange, "location", location = location, ang = ang)
    return (location, ang)
"""


def findClosestDot(lidardists, minv, maxv, mode, location, ang = None):
    variance = np.array(list(range(minv, maxv + 1)))
    difvsret = {}
    if mode == "location":
        xs = variance.copy() + location[0]
        ys = variance.copy() + location[1]
        for x in xs:
            for y in ys:
                testdists = CythonLidarPost.angledRayIntersects(CythonLidarPost.Point(x, y), ang)
                difvsret[findDotDif(lidardists, testdists)] = (x, y)  # findDotDif finds the dot sum of the arguments
    if mode == "angle":
        for var in variance:
            testdists = CythonLidarPost.angledRayIntersects(CythonLidarPost.Point(location[0], location[1]), var)
            difvsret[findDotDif(lidardists, testdists)] = var
    return difvsret[sorted(difvsret)[-1]]
    # return difvsret[sorted(difvsret)[0]]


#
def accountForObstacles(distdifs, obstacles):
    obstangles = []
    for angle in distdifs:
        for obst in obstacles:
            if angle >= obst[0] and angle <= obst[1]:
                obstangles.append(angle)
    for angle in obstangles:
        distdifs.pop(angle)
    return distdifs


def parseLidar(lidarid):
    pass


def findDotDif(lidardists, idealdists):
    #- Uncoment out
    idealdists = np.array(list(idealdists.values()))
    lidardists = np.array(list(lidardists.values()))
    csum = np.dot(lidardists, lidardists)
    realsum = np.dot(idealdists, lidardists)
    return abs(csum - realsum)


def findDistDifs(lidardists, idealdists):
    distdifs = {} 
    for ang in idealdists:
        distdifs[ang] = idealdists[ang] - lidardists[ang]
    return distdifs


def findKeysInCommon(maindict, testingdict):
    mainkeys = list(maindict.keys())
    testkeys = list(testingdict.keys())
    commonkeys = list(set(mainkeys).intersection(set(testkeys)))
    commonvals = {ckey: maindict[ckey] for ckey in commonkeys}
    return commonvals


def shiftKeys(shifted, offset):
    keys = [key for key in shifted]
    vals = [shifted[key] for key in shifted]
    shiftedkeys = []
    for key, ind in enumerate(keys):
        shiftedkeys.append(keys[(ind + offset) % len(keys)])
    for ind, key in enumerate(shiftedkeys):
        shifted[key] = vals[ind]
    return shifted


def calcDotSum(ideal, real):
    # dotsum = 0
    # for key in ideal:
    #     dotsum += ideal[key] * real[key]
    ideal = sortDictByVal(ideal)
    real = sortDictByVal(real)
    ideals = np.array(list(ideal.values()))
    reals = np.array(list(real.values()))
    dotsum = (ideals * reals).sum()
    return dotsum


def sortDictByVal(testdict):
    newkeys = sorted(testdict)
    newdict = {}
    for key in newkeys:
        newdict[key] = testdict[key]
    return newdict


def dotSvg(pointvals, location):
    largestpoint = []
    pointdist = 0
    svg = open("dotgraph.svg", "w")
    svg.write("""<!DOCTYPE html>
                  <html>
                  <body>
                  """)
    svg.write('<svg height = "{0}" width = "{1}">\n'.format(700, 700))
    for point in pointvals:
        if pointvals[point] > pointdist:
            largestpoint = point
            pointdist = pointvals[point]
        svg.write('<circle cx = "{0}" cy = "{1}" r = "{2}" '
                  'stroke = "black" stroke-width = "3" '
                  'fill = "red"/>\n'.format((point[0] - 46) * 80, (point[1] - 46) * 80,
                                            round((pointvals[point] - 9000000)/10000)))
        # print(point, pointvals[point])
    svg.write('<circle cx = "{0}" cy = "{1}" r = "5" '
                'stroke = "blue" stroke-width = "3" fill = "blue"/>\n'.format((location[0] - 46) * 80,
                                                                            (location[1] - 46) * 80))
    svg.write('<circle cx = "{0}" cy = "{1}" r = "2" '
                'stroke = "yellow" stroke-width = "3" fill = "yellow"/>\n'.format((largestpoint[0] - 46) * 80,
                                                                            (largestpoint[1] - 46) * 80))
    svg.write("""<\svg>
                 <\\body>
                 <\html>""")
    svg.close()


def findLargestPointPerAngle(anglepoints):
    points = {}
    for anglepoint in anglepoints:
        if anglepoints[anglepoint][0] in points:
            if anglepoint > points[anglepoints[anglepoint][0]]:
                points[anglepoints[anglepoint][0]] = anglepoint
        else:
            points[anglepoints[anglepoint][0]] = anglepoint
    return points


def speedThisProgramUpDramatically():
    postpoints = {}
    xs = range(1, 324)
    ys = range(1, 648)
    angs = range(360)
    for x in xs:
        for y in ys:
            for ang in angs:
                postpoints[(x, y, ang)] = CythonLidarPost.angledRayIntersects(CythonLidarPost.Point(x, y), ang)
    json.dump(postpoints, "postpoints.json")


x = CythonLidarPost.pointFromDistAng(CythonLidarPost.Point(150, 150), 45, 8)
print(x.x, x.y)

def shiftInds(itershift, offset):
    return np.concatenate((itershift[offset:], itershift[:offset]))
    # return itershift[offset:] + itershift[:offset]

def measureTime(func):
    start = time.time()
    func()
    fin = time.time()
    finaltime = fin - start
    print("Time: {0}".format(finaltime))

def main():
    realpoints = [50, 48]
    testval = shiftInds(CythonLidarPost.angledRayIntersects(CythonLidarPost.Point(realpoints[0], realpoints[1]), 0, CythonLidarPost.openEnvFile("FRC_Field_2018.map")), 7,)
    printinfo, pointvals = findBestLocation(testval, [49, 49, 2], 5, 15)
    # print(printinfo)
    dotSvg(findLargestPointPerAngle(pointvals), realpoints)


# speedThisProgramUpDramatically()

# cProfile.run("main()")
print(CythonLidarPost.customRayIntersects(CythonLidarPost.Point(100, 100), [1], CythonLidarPost.openEnvFile("FRC_Field_2018.map")))
