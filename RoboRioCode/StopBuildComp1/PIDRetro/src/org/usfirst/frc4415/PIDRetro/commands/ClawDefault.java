// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.PIDRetro.commands;
import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc4415.PIDRetro.Robot;

/**
 *
 */
public class ClawDefault extends Command {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public ClawDefault() {

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
        requires(Robot.clawPID);

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    }

    // Called just before this Command runs the first time
    @Override
    protected void initialize() {
    }

    // Called repeatedly when this Command is scheduled to run
    @Override
    protected void execute() {
    	
    	if (Robot.oi.getDriverJoystick().getRawButton(3)) {
    		Robot.clawPID.clawClose();
    	}
    	
    	if (Robot.oi.getDriverJoystick().getRawButton(4)) {
    		Robot.clawPID.clawOpen();
    	}
    	
    	if (Robot.oi.getDriverJoystick().getRawAxis(2) < .3 && Robot.oi.getDriverJoystick().getRawAxis(3) < .3) {
    		Robot.clawPID.wristOff();
    	} else {
    		Robot.clawPID.wristUp();
        	Robot.clawPID.wristDown();
    	}
    	
    	if (Robot.oi.getDriverJoystick().getPOV() == -1) {
    		Robot.clawPID.wheelOff();
    	} else {
    		Robot.clawPID.wheelIn();
    		Robot.clawPID.wheelOut();
    	}
    	
    	/*if (Robot.clawPID.getLimitSwitch()) {
    		Robot.clawPID.wristDown();
    	}*/
    	
    }

    // Make this return true when this Command no longer needs to run execute()
    @Override
    protected boolean isFinished() {
        return false;
    }

    // Called once after isFinished returns true
    @Override
    protected void end() {
    }

    // Called when another command which requires one or more of the same
    // subsystems is scheduled to run
    @Override
    protected void interrupted() {
    }
}