# RobotCode2018

Autonomous code for the robot.

## Description

The program is divided into two parts:

- Pathfinding, and
- Robot Control

Robot Control is Java code run on the RoboRio—it interacts directly with the Driver-Station and with the Raspberry Pi Co-Processor.
Pathfinding uses LIDAR to continually report and correct the robot's orientation on the field, passing location information to the RobotControl program. It also gives the RobotControl program instructions to guide its movement.

### Required libraries

- [NumPy](http://www.numpy.org/)
- [OpenCV](https://opencv.org/)
- [pySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html)

#### Communication between these devices and programs works as follows

1. AUTO Starts
2. DriverStation sends pathing information to RoboRio (RobotControl), which then forwards that information to the coprocessor (Pathfinding).
3. Pathfinding calculates the proper movements the robot needs to make to complete the tasks, and passes movement commands back to RobotControl.
4. The robot begins to move! Pathfinding uses LIDAR and additional measurements to provide any corrective information to the robot's movement.
5. The robot arrives at it's location / completes the assigned tasks.
6. AUTO ends, and TELEOP begins.
7. RobotControl listens to commands from the DriverStation to move the robot and its various manipulators, while PathFinding records sensor ata for after-match review.

#### A more detailed overview of program flow

*Abbreviations and their meanings:*

- FMS: Field Management System
- DS: DriverStation
- Rio: RoboRio and its associated Robot Control software
- Pi: Raspberry Pi Co-Processor and its associated Pathfinding software

*Program flow:*

1. DS > Rio: `X,Y,LLL,NearSwitch,Deliver,Collect,Scale,Deliver`
2. Rio > Pi: `X,Y,LLL,NearSwitch,Deliver,Collect,Scale,Deliver`
3. Pi: "`X,Y` are the expected starting coordinates".
4. Pi: "`LLL` is the distribution of the colors on the scales and the switch".
5. Pi: "`NearSwitch,Deliver,Collect,Scale,Deliver` is the pathing instruction set".
6. Pi: Calculate optimal route.
7. Proceed along route, and observe offset between expected and actual LIDAR measurements caused by motor drift.
8. Pi > Rio: `X,D`
9. Rio: "`X` is the target distance and direction."
10. Rio: "`D` is the offset rotation in degrees."