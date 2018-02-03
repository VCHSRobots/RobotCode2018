# speed.pyx: Writes postulated fieldpoints points to a json file
# 1-6-2018

import cysimlidar
import json
import atexit
import numpy


size = [324, 360]

global lastxy


xy = open("lastxy.json")
lastxy = json.load(xy)
xy.close()


cpdef speedUp():
    global lastxy
    jdict = {}
    postpoints = {}
    completed = lastxy[0]
    xs = range(1, size[0])
    ys = range(1, size[1])
    times = len(xs)
    cdef int vtimes = 0
    for x in xs:
        if x < completed:
            vtimes += 1
            continue
        for y in ys:
            postpoints["({0}, {1})".format(x, y)] = cysimlidar.angledRayIntersects(cysimlidar.Point(x, y), 0)
        vtimes += 1
        print("{0}/{1} Postulations Complete".format(vtimes, times))
        jf = open("postulations{0}.json".format(x), "w")
        json.dump(postpoints, jf, indent=2)
        jf.close()
        lastxy = (x, y)
        postpoints = {}
    print("Postulation successful!")


cdef lastfunc():
    global lastxy
    xy = open("lastxy.json", "w")
    json.dump(lastxy, xy)
    xy.close()


atexit.register(lastfunc)

# "Size": [324, 648]
# C:\Users\Public\Holiday\PycharmProjects
# python setup.py build_ext --inplace
