"""Log.py performs logging functions.

Log.py takes logging information and places it into the "Logging" directory as a file.
"""

#
# Built-in imports.
#

import sys
import time
from uuid import uuid4

#
# Custom imports.
#

import Configuration

#
# Global variables.
#

Config = Configuration.LoadConfig()

#
# Functions.
#

def Log(Message = None, LogLevel = 1):
    if Message == None:
        raise ValueError("Message has no value.")
    Time = time.strftime("%Y-%m-%d %H:%M:%S")
    LogLevel = str(LogLevel).lower()
    if LogLevel in ("0", "debug"):
        if Config["LogDebugMessages"]:
            Message = "DEBUG:    {0}".format(Message)
        else:
            return
    elif LogLevel in ("1", "info"):
        Message = "INFO:     {0}".format(Message)
    elif LogLevel in ("2", "warning"):
        Message = "WARNING:  {0}".format(Message)
    elif LogLevel in ("3", "error"):
        Message = "ERROR:    {0}".format(Message)
    elif LogLevel in ("4", "critical"):
        Message = "CRITICAL: {0}".format(Message)
    else:
        raise ValueError("Improper value passed for log level.")
    Message = "{0} > {1}".format(Time, Message)
    print(str(Message))
    with open(Config["LogFile"], "a") as File:
        File.write(Message + "\r\n")

#
# Mainline code.
#

if __name__ == "__main__":
    sys.exit("This file may not be run as a standalone.")