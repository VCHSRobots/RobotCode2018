# parselidar.py: Outputs difference between ideal and actual lidar data
# 1-18-2018

import numpy as np
import cProfile
import cysimlidar
import time
import json

size = [324, 360]

def catctMyDrift(lidarid, location, robotangle):
    lidardists = parseLidar(lidarid)
    idealdists = cysimlidar.angledRayIntersects(cysimlidar.Point(location[0], location[1]), robotangle)
    realloc, null = findBestLocation(lidardists, idealdists, location, np.array([-30, 30]))


def findBestLocation(lidardists, location, testingrange, angoffsetrange):
    difvsret = {}
    cordrange = np.array([[location[0] - testingrange, location[0] + testingrange],
                         [location[1] - testingrange, location[1] + testingrange]])
    cordrange[cordrange <= 0] = 1
    cordx = cordrange[0]
    cordy = cordrange[1]
    cordx[cordx >= size[0]]  = size[0] - 1
    cordy[cordy >= size[1]]  = size[1] - 1
    cordrange = np.array([cordx[0], cordx[1], cordy[0], cordy[1]])
    xs = tuple(range(cordrange[0], cordrange[1] + 1))
    ys = tuple(range(cordrange[2], cordrange[3] + 1))
    angs = tuple(range(location[2] - angoffsetrange, location[2] + angoffsetrange + 1))
    posts = openPosts(cordrange)
    for x in xs:
        for y in ys:
            postdists = posts["({0}, {1})".format(x, y)]
            for angle in angs:
                testdists = shiftInds(postdists, angle)
                # distdifs = findDistDifs(lidardists, idealdists)
                # lidardists = accountForObstacles(lidardists, measureObstacles(distdifs, sensitivity = 20))
                difvsret[findDotDif(lidardists, testdists)] = [(x, y), angle]
                # difvsret[np.dot(np.array(lidardists), np.array(testdists))] = [(x, y), angle]
    bestdotdif = difvsret[sorted(difvsret)[0]]
    # bestdotdif = difvsret[sorted(difvsret)[-1]]
    reallocation = bestdotdif[0]
    ang = bestdotdif[1]
    return (reallocation, ang), difvsret


def openPosts(cordrange):
    """
    Range of cordinates -> One opened dict of needed cordinates
    Will only need x cordinates (one file has one x cordinates but contains all ys as of now)
    """
    x = cordrange[0]
    posts = {}
    while x <= cordrange[1]:
        fn = "postulations{0}.json".format(x)
        pfile = open(fn)
        prange = json.load(pfile)
        posts.update(prange)
        pfile.close()
        x += 1
    return posts


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
    idealdists = np.array(idealdists) # findIndexesInCommon(idealdists, lidardists))
    lidardists = np.array(lidardists)
    realprod = np.dot(lidardists, lidardists)
    dotprod = np.dot(idealdists, lidardists)
    return abs(dotprod - realprod)


def findDistDifs(lidardists, idealdists):
    distdifs = {}
    # idealdists = findIndexesInCommon(idealdists, lidardists)
    for ang in idealdists:
        if ang is not None:
            distdifs[ang] = idealdists[ang] - lidardists[ang]
    return distdifs


# def findIndexesInCommon(mainlist, testinglist):
#     for ind, val in enumerate(testinglist):
#         if val is None:
#             mainlist[ind] = None
#     return mainlist


def shiftInds(itershift, offset):
    return itershift[offset:] + itershift[:offset]


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
    testfile = open("postulations{0}.json".format(realpoints[0]))
    testval = json.load(testfile)["({0}, {1})".format(realpoints[0], realpoints[1])]
    testfile.close()
    printinfo, pointvals = findBestLocation(testval, [49, 49, 30], 10, 30)
    print(printinfo)
    # dotSvg(findLargestPointPerAngle(pointvals), realpoints)

cProfile.run("main()")

# With Numpy calculations

