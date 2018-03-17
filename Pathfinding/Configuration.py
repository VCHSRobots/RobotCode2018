# -*- coding: utf8 -*-

"""Configuration.py

Configuration.py parses the configuration file ("Pathfinding.cfg") for all modules.
"""

#
# Built-in imports.
#

import json
import sys

#
# Functions.
#

def LoadConfig():
    """
    Loads configuration data from the file Pathfinding.cfg.
    """
    with open("Pathfinding.cfg", "r") as File:
        Config = json.load(File)
    return Config

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")
