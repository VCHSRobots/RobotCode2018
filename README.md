# RobotCode2018
Autonomous code for the robot.
## Description:
The program is divided into two parts:
 - Pathfinding, and
 - Robot Control  
Robot Control is Java code run on the RoboRio—it interacts directly with the Driver-Station and with the Raspberry Pi Co-Processor.  
Pathfinding uses LIDAR to continually report and correct the robot's orientation on the field, passing location information to the RobotControl program. It also gives the RobotControl program instructions to guide its movement.  
### Required libraries:
 - [OpenCV](https://opencv.org/)
 - [NumPy](http://www.numpy.org/)
#### Communication between these devices and programs works as follows:
 0. AUTO Starts
 1. DriverStation sends pathing information to RoboRio (RobotControl), which then forwards that information to the coprocessor (Pathfinding).
 2. Pathfinding calculates the proper movements the robot needs to make to complete the tasks, and passes movement commands back to RobotControl.
 3. The robot begins to move! Pathfinding uses LIDAR and additional measurements to provide any corrective information to the robot's movement.
 4. The robot arrives at it's location / completes the assigned tasks.
 5. AUTO ends, and TELEOP begins.
 6. RobotControl listens to commands from the DriverStation to move the robot and its various manipulators, while PathFinding records sensor data for after-match review.
#### A more detailed overview of program flow:
*Abbreviations and their meanings:*
 - FMS: Field Management System
 - DS: DriverStation
 - Rio: RoboRio and its associated Robot Control software
 - Pi: Raspberry Pi Co-Processor and its associated Pathfinding software
*Program flow:*
 0. DS > Rio: `X,Y,LLL,NearSwitch,Deliver,Collect,Scale,Deliver`
 1. Rio > Pi: `X,Y,LLL,NearSwitch,Deliver,Collect,Scale,Deliver`
 2. Pi: "`X,Y` are the expected starting coordinates".
 3. Pi: "`LLL` is the distribution of the colors on the scales and the switch".
 4. Pi: "`NearSwitch,Deliver,Collect,Scale,Deliver` is the pathing instruction set".
 5. Pi: Calculate optimal route.
 6. Proceed along route, and observe offset between expected and actual LIDAR measurements caused by motor drift.
 7. Pi > Rio: `X,Y,D`
 8. Rio: "`X, Y` are the offset in inches."
 9. Rio: "`D` is the offset rotation in degrees."
