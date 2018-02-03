# speed.pyx: Writes postulated fieldpoints points to a json file
# 1-6-2018

import cysimlidar
import json
import atexit
import numpy


size = [324, 360]

global jdict
global lastxy


xy = open("lastxy.json")
lastxy = json.load(xy)
print(lastxy)
xy.close()


def speedUp():
    global jdict
    global lastxy
    completed = [lastxy[0], lastxy[1]]
    postpoints = {}
    xs = range(1, size[0])
    ys = range(1, size[1])
    angs = range(360)
    times = len(xs) * len(ys)
    vtimes = 0
    for x in xs:
        if x < completed[0]:
            continue
        for y in ys:
            if x == completed[0] and y < completed[1]:
                continue
            for ang in angs:
                postpoints["({0}, {1}, {2})".format(x, y, ang)] = cysimlidar.angledRayIntersects(cysimlidar.Point(x, y), ang)
            print("{0}/{1} Postulations Complete".format(x * y, times))
            vtimes += 1
            jdict.update(postpoints)
            jf = open("postulations{0}_{1}.json".format(x, y), "w")
            json.dump(jdict, jf, indent=2)
            jf.close()
            lastxy = (x, y)
    print("Postulation successful!")


def lastfunc():
    global lastxy
    xy = open("lastxy.json", "w")
    json.dump(lastxy, xy)
    xy.close()


atexit.register(lastfunc)

# "Size": [324, 648]
# C:\Users\Public\Holiday\PycharmProjects
# python setup.py build_ext --inplace
