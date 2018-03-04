import serial
import math
import numpy as numpy
import struct
import time

from LIDAR import Compare, GetExpectedData
from Render import RenderPoints

SweepLocation = "COM6"

Sweep = serial.Serial(SweepLocation, baudrate=115200, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False, rtscts=False, dsrdtr=False)
Sweep.write(b"ID\n")
print("Version requested.")
Response = Sweep.readline().decode("utf-8")
print("Response: {0}".format(Response))
print("Starting scanning...")
Sweep.write(b"DS\n")
Response = Sweep.readline().decode("utf-8")
assert (len(Response) == 6), "Bad data."

Status = Response[2:4]
if Status == "00":
    print("Status is OK!")
else:
    print("Status is NOT OK: {0}".format(Status))

Format = "=" + "B" * 7

Data = ()

Log = open("sweep.csv", "wb")
Log.write("angle, distance, x, y\n".encode())

try:
    while True:
        Line = Sweep.read(7)
        assert (len(Line) == 7), "Bad data read: {0}".format(len(Line))
        Data = struct.unpack(Format, Line)
        print("RawData: {0}".format(Data))
        assert (len(Data) == 7), "Bad data type conversion: {0}".format(len(Line))
        AzimuthLow = Data[1]
        AzimuthHigh = Data[2]
        AngleInt = (AzimuthHigh << 8) + AzimuthLow
        Degrees = (AngleInt >> 4) + (AngleInt & 15) / 16
        DistanceLow = Data[3]
        DistanceHigh = Data[4]
        Distance = ((DistanceHigh << 8) + DistanceLow) / 100
        X = Distance * math.cos(Degrees * math.pi / 180)
        Y = Distance * math.sin(Degrees * math.pi / 180)
        Log.write("%f, %f, %f, %f\n".encode() % (Degrees, Distance, X, Y))
except KeyboardInterrupt as e:
    pass
finally:
    print("Stop scanning.")
    Sweep.write(b"DX\n")
    Response = Sweep.read().decode("utf-8")
    print("Response: {0}".format(Response))