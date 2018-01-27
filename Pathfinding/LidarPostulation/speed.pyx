# speed.pyx: Writes postulated fieldpoints points to a json file
# 1-6-2018

import cysimlidar
import json
import atexit

size = [324, 360]

postf = open("postulations.json")
global jdict
jdict = json.load(postf)
postf.close()
global lastxy

cdef speedThisProgramUpDramatically(list completed):
    postpoints = {}
    xs = range(1, size[0])
    ys = range(1, size[1])
    angs = range(360)
    times = len(xs) * len(ys)
    vtimes = 0
    jdict = json.load("postulations.json")
    for x in xs:
        if x < completed[0]:
            continue
        for y in ys:
            if x == completed[0] and y > completed[1]:
                continue
            print("{0}/{1} Postulations Complete".format(vtimes, times))
            vtimes += 1
            for ang in angs:
                postpoints[(x, y, ang)] = cysimlidar.angledRayIntersects(cysimlidar.Point(x, y), ang)
            jdict.update(postpoints)
            lastxy = (x, y)
    print("Postulation successful!")


def lastfunc():
    json.dump(jdict, "postulations.json")
    json.dump(lastxy, "lastxy.json")


atexit.register(lastfunc)

# "Size": [324, 648]
# C:\Users\Public\Holiday\PycharmProjects
# python setup.py build_ext --inplace
