# speed.pyx: Writes postulated fieldpoints points to a json file
# 1-6-2018

import cysimlidar
import json

size = [324, 360]

cdef saveSeg(tuple rangex, tuple rangey, str outfile):
    postpoints = {}
    xs = range(rangex[0], rangex[1])
    ys = range(rangey[0], rangey[1])
    angs = range(360)
    times = len(xs) * len(ys)
    vtimes = 0
    for x in xs:
        for y in ys:
            print("{0}/{1} Postulations Complete".format(vtimes, times))
            vtimes += 1
            for ang in angs:
                postpoints[(x, y, ang)] = cysimlidar.angledRayIntersects(cysimlidar.Point(x, y), ang)
            jdict = json.load(outfile)
            jdict.update(postpoints)
            json.dump(jdict, outfile)
    print("Postulation successful!")


def speedThisProgramUpDramatically(chunksize, chunksdone = 0):
    xchunks = size[0]//chunksize
    ychunks = size[1]//chunksize
    leftoverchunks = [size[0] - xchunks, size[1] - ychunks]
    for val in range(chunksize):
        if val <= chunksdone:
            continue
        x = (val * xchunks, (val + 1) * xchunks)
        y = (val * ychunks, (val + 1) * ychunks)
        saveSeg(x, y, "post.json".format(val))
        print(val)
    saveSeg((xchunks * chunksize, xchunks * (chunksize + leftoverchunks[0])),
            (ychunks * chunksize, ychunks * (chunksize + leftoverchunks[1])),
            "post.json".format(chunksize))



# "Size": [324, 648]
# C:\Users\Public\Holiday\PycharmProjects
# python setup.py build_ext --inplace
