# -*- coding: utf8 -*-

"""Master.py

Master.py handles communication between itself and the RoboRio code, and coordinates calls to Pathfinding.py and LIDAR.py
"""

#
# Built-in imports.
#

import atexit
import json
import sys

#
# Custom imports.
#

import Configuration
import LIDAR
from Log import Log
import Pathfinding
from Render import Render

#
# Global variables.
#

Config = Configuration.LoadConfig()
DistanceTraversed = 0
Instructions = ""
MapData = None
NumberOfPositionEvaluations = 0

#
# Classes and Functions.
#

class Communicate:
    def Connect():
        pass
    def Receive():
        global Instructions
        # Something will go here that listens continually for data.
        if Data[0].lower() == "e": # If the data received is an encoder increment notice
            DistanceTraversed += 1 / Config["EncoderRotatonsPerInch"]
        elif Data[0].lower() == "i": # If the data received is an instruction set:
            Log("Received pathfinding instruction set from remote server.")
            Instructions = Data
        else:
            Log("Incorrect header \"{0}\" received from remote server.".format(Data[0].lower()), 3)
    def Send():
        pass

def DisplayConfigurationMenu():
    print("// Command-line configuration is not yet implemented. Edit the configuration file \"Pathfinding.cfg\" manually to modify program settings.")
    sys.exit()

def Exit():
    Log("Pathfinding system stopped.", 1)

def Move(Instructions):
    global DistanceTraversed
    global MapData
    global NumberOfPositionEvaluations
    ParsedInstructions = Pathfinding.ParseInstructions(Instructions)
    if not MapData: # If we have yet to load any map data.
        with open(Config["MapSource"]) as File:
            MapData = json.load(File)
            MapData = Pathfinding.ExpandMapElements(MapData)
            Render(MapData, "Initial Map Render")
            NumberOfPositionEvaluations += 1
    CurrentPosition, CurrentRotation, AnomalousElements = LIDAR.GetCurrentData()
    if AnomalousElements: # If any anomalous elements were detected in the LIDAR scans.
        MapData["Elements"].extend(AnomalousElements)
        MapData = Pathfinding.ExpandMapElements(MapData)
    PathInformation = Pathfinding.Path(MapData, ParsedInstructions["CurrentPosition"], ParsedInstructions["ElementDistribution"], ParsedInstructions["PathList"])
    Render(MapData, None, PathInformation)
    for Item in PathInformation:
        if type(Item) is str: # If the path item is an action.
            PerformAction(Item.lower(), CurrentPosition)
        else: # If the path item is a point to travel to.
            while DistanceTraversed < 100: # TODO: Do this!
                # Begin moving toward point.
                # TODO: Convert "steps" (two pairs of points) to vectors for calculating progression along path.
                PathInformation = Pathfinding.VectorizePathInformation(PathInformation)
                DistanceTraversed += 1
                # Communicate.Send("") # Send direction command to RoboRio.

def ParseUserInput():
    Input = [X.lower() for X in sys.argv[1:]]
    if len(Input) < 1:
        Log("No command-line user input received.", 0)
        return
    Log("Verbatim command-line user input: " + str(Input), 0)
    if any(X in Input[0] for X in ("-h", "-?")):
        print("// Pathfinding help menu:\r\n// Commands:\r\n// -h, --help, -?\t Help Information\r\n// -c, --configure\tConfiguration Menu\r\n// --modify-password-visibility\tProcure BASH information.\r\n// Documentation:\r\n// You may view documentation locally at FILENAME, or online at either https://github.com/VCHSRobots/RobotCode2018, or at mirror http://pkre.co/RobotCode2018.")
        sys.exit()
    elif any(X in Input[0] for X in ("-c", "-s")):
        DisplayConfigurationMenu()
        return
    elif Input[0] == "--modify-password-visibility":
        print("// http://bash.org/?244321")
        sys.exit()
    else:
        print("Unable to parse command-line user input. Use \"-h\" for help.")
        sys.exit()

def PerformAction(Action, CurrentLocation):
    if Action == "deliver":
        pass # Perform the mechanics for delivering a power cube to the nearest location.
    elif Action == "collect":
        pass # Perform the mechanics for collecting a power cube from the nearest power-cube-location.

#
# Mainline code.
#

atexit.register(Exit)
Log("Pathfinding system initialized.", 1)
ParseUserInput()

# Attempt to establish connection with RoboRio software.
Communicate.Connect()

# Receive initial pathfinding instruction set either from remote server or file.
if Config["InstructionSource"].lower() in ("remote", "server", "roborio"):
    Log("Receiving pathfinding instruction set from remote server.", 0)
    while Instructions == "": # Wait for instructions to be updated.
        pass
else:
    File = Config["InstructionSource"]
    Log("Loading pathfinding instruction set from file \"{0}\".".format(File), 0)
    with open(File, "r") as File:
        Instructions = File.read()

# Move
Move(Instructions)
