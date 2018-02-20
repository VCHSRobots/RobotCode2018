# SweepCommunication.py: Making library for communication with the Sweep lidar
# HP 2/17/2018

def checkMotorInfo(sweep):
    sweep.write(b"IV\n")
    return sweep.readline()

def checkMotorInfo(sweep):
    sweep.write(b"ID\n")
    return sweep.readline()

def resetSweep(sweep):
    sweep.write(b"RR\n")
    return sweep.readline()

def getData(sweep, itertimes):
    for null in range(itertimes):
        data = sweep.readline()
        yield parseSweepScannedBytesInDict(data)

def parseSweepScannedBytesInDict(sweepbytes):
    sweepscans = {}
    azimuth = []
    distance = []
    for ind, byte in enumerate(sweepbytes):
        if ind == 0:
            sweepscans["sync"] = byte
        elif ind == 1:
            azimuth.append(byte)
        elif ind == 2:
            azimuth.append(byte)
            floatazimuth = (azimuth[1] << 8) + azimuth[0]
            convertedazimuth = floatazimuth/16
            sweepscans["angle"] = convertedazimuth
        elif ind == 3:
            distance.append(byte)
        elif ind == 4:
            distance.append(byte)
            intdistance = (distance[1] << 8) + distance[0]
            sweepscans["distance"] = intdistance
        elif ind == 5:
            sweepscans["sigstrength"] = byte
        elif ind == 6:
            sweepscans["checksum"] = byte
    print(sweepscans)
    return sweepscans

def adjustMotorSpeed(sweep, speed):
    strspeed = str(speed)
    sweep.write(bytes("MZ{0:02}\n".format(rate), "ascii"))
    return sweep.readline()

def adjustSampleRate(sweep, rate):
    sweep.write(bytes("LR{0:02}\n".format(rate), "ascii"))
    return sweep.readline()

def testScanData():
    sweep = makeSweep("COM3")
    # adjustSampleRate(sweep, 3)
    time.sleep(3)
    startScan(sweep)
    data = getData(sweep, 10)
    for dict in data:
        if dict["sync"] == 0 or dict["sync"] == 1:
            print(dict["angle"], dict["distance"])
    stopScan(sweep)
