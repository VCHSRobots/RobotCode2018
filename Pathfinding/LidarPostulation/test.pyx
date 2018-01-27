# parselidar.py: Outputs difference between ideal and actual lidar data
# 1-18-2018

import numpy as np
import cProfile
import simulatelidar
import time

def catctMyDrift(lidarid, location, robotangle):
    lidardists = parseLidar(lidarid)
    idealdists = simulatelidar.angledRayIntersects(simulatelidar.Point(location[0], location[1]), robotangle)
    realloc, null = findBestLocation(lidardists, idealdists, location, np.array([-30, 30]))



def findBestLocation(lidardists, location, testingrange, angoffsetrange):
    difvsret = {}
    xs = tuple(range(location[0] - testingrange, location[0] + (testingrange + 1)))
    ys = tuple(range(location[1] - testingrange, location[1] + (testingrange + 1)))
    angs = tuple(range(angoffsetrange[0], angoffsetrange[1] + 1))
    for x in xs:
        for y in ys:
            for angle in angs:
                idealdists = simulatelidar.angledRayIntersects(simulatelidar.Point(x, y), angle)
                # distdifs = findDistDifs(lidardists, idealdists)
                # lidardists = accountForObstacles(lidardists, measureObstacles(distdifs, sensitivity = 20))
                difvsret[findDotDif(lidardists, idealdists)] = [(x, y), angle]
    bestdotdif = difvsret[sorted(difvsret)[-1]]
    reallocation = [bestdotdif[0]]
    ang = bestdotdif[1]
    return (reallocation, ang), difvsret


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
                testdists = simulatelidar.angledRayIntersects(simulatelidar.Point(x, y), ang)
                difvsret[findDotDif(lidardists, testdists)] = (x, y)  # findDotDif finds the dot sum of the arguments
    if mode == "angle":
        for var in variance:
            testdists = simulatelidar.angledRayIntersects(simulatelidar.Point(location[0], location[1]), var)
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
    idealdists = np.array(list(sortDictByVal(findKeysInCommon(idealdists, lidardists)).values()))
    lidardists = np.array(list(sortDictByVal(lidardists).values()))
    # idealsum = np.dot(idealdists, idealdists)
    realsum = np.dot(idealdists, lidardists)
    # Keep comented out
    # # idealsum = calcDotSum(idealdists, idealdists)
    # # realsum = calcDotSum(lidardists, idealdists)
    # End keep comented out
    # sumdif = idealsum - realsum
    # if sumdif < 0:
    #     print("Smaller:", sumdif)
    # elif sumdif > 0:
    #     print("Bigger:", sumdif)
    # return abs(sumdif)
    #- End uncoment out
    return realsum


def findDistDifs(lidardists, idealdists):
    distdifs = {}
    idealdists = findKeysInCommon(idealdists, lidardists)
    for ang in idealdists:
        distdifs[ang] = idealdists[ang] - lidardists[ang]
    return distdifs


def findKeysInCommon(maindict, testingdict):
    mainkeys = list(maindict.keys())
    testkeys = list(testingdict.keys())
    commonkeys = list(set(mainkeys).intersection(set(testkeys)))
    commonvals = {ckey: maindict[ckey] for ckey in commonkeys}
    return commonvals


"""
def shiftKeys(shifted, offset):
    keys = [key for key in shifted]
    vals = [shifted[key] for key in shifted]
    shiftedkeys = []
    for key, ind in enumerate(keys):
        shiftedkeys.append(keys[(ind + offset) % len(keys)])
    for ind, key in enumerate(shiftedkeys):
        shifted[key] = vals[ind]
    return shifted
"""


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


#
def measureObstacles(distdifs, sensitivity = 1):
    obstacle = 0
    obstacles =[]
    for ang in distdifs:
        distdif = distdifs[ang]
        if distdif >= sensitivity:
            obstacle += 1
        else:
            obstacle = 0
        if obstacle:
            if obstacle == 1:
                obstacles.append([ang, ang, {ang: distdif}])
            else:
                obstacles[-1][1] = ang
                obstacles[-1][2][ang] = distdif
    return obstacles


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
        print(point, pointvals[point])
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


def measureTime(func):
    start = time.time()
    func()
    fin = time.time()
    finaltime = fin - start
    print("Time: {0}".format(finaltime))

def main():
    realpoints = [50, 48]
    testval = simulatelidar.angledRayIntersects(simulatelidar.Point(realpoints[0], realpoints[1]), 7)
    printinfo, pointvals = findBestLocation(testval, [49, 49], 2, [-10, 10])
    print(printinfo)
    dotSvg(findLargestPointPerAngle(pointvals), realpoints)


cProfile.run("main()")
# With Numpy calculations
