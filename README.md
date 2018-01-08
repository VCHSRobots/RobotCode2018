# RobotCode2018
Autonomous code for the robot.
## Description:
The program is divided into two parts:
 - Pathfinding, and
 - Robot Control
Robot Control is Java code run on the RoboRio - it interacts directly with the Driver-Station and with the Raspberry Pi Co-Processor.  
Pathfinding uses LIDAR to continually report and correct the robot's orientation on the field, passing location information to the RobotControl program. It also gives the RobotControl program instructions to guide its movement.  
### Communication between these devices and programs is as follows:
 0. AUTO Starts
 1. DriverStation sends pathing information to RoboRio (RobotControl), which then forwards that information to the coprocessor (Pathfinding).
 2. Pathfinding calculates the proper movements the robot needs to make to complete the tasks, and passes movement commands back to RobotControl.
 3. The robot begins to move! Pathfinding uses LIDAR and additional measurements to provide any corrective information to the robot's movement.
 4. The robot arrives at it's location / completes the assigned tasks.
 5. AUTO ends, TELEOP begins.
 6. RobotControl listens to commands from the DriverStation to move the robot and its various manipulators, while PathFinding records sensor data for after-match review.