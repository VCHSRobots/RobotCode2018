// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.RetroFinal.commands;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.command.Command;

import java.util.concurrent.TimeUnit;

import org.usfirst.frc4415.RetroFinal.Robot;

/**
 *
 */
public class AutoLeftScaleCommand extends Command {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
	
	String gameData;

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutoLeftScaleCommand() {
    	setRunWhenDisabled(true);

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_SETTING
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=REQUIRES
    }

    // Called just before this Command runs the first time
    @Override
    protected void initialize() {
    	
    }

    // Called repeatedly when this Command is scheduled to run
    @Override
    protected void execute() {
    	
    	gameData = DriverStation.getInstance().getGameSpecificMessage();
    	
    	if (gameData.length() > 0) {
    		
    		if (gameData.charAt(1) == 'L') {
    			Robot.driveTrainPID.enable();
    			Robot.driveTrainPID.setSetpoint(2300);
    			Robot.wedgeArmPID.enable();
    			Robot.wedgeArmPID.setSetpoint(80);
    			Robot.clawPID.setSetpoint(20);
    			Robot.telescopePID.enable();
    			Robot.telescopePID.setSetpoint(220);
    			
    			try {
    				TimeUnit.SECONDS.sleep(5);
    			} catch (InterruptedException e) {
    				// TODO Auto-generated catch block
    				e.printStackTrace();
    			}
    			
    			Robot.driveTrainPID.turnLeftAngle(45, .6, .7, .6, true);
    			
    			try {
    				TimeUnit.SECONDS.sleep(3);
    			} catch (InterruptedException e) {
    				// TODO Auto-generated catch block
    				e.printStackTrace();
    			}
    			
    			Robot.clawPID.enable();
    			Robot.clawPID.setSetpoint(140);
    			
    			try {
    				TimeUnit.SECONDS.sleep(4);
    			} catch (InterruptedException e) {
    				// TODO Auto-generated catch block
    				e.printStackTrace();
    			}
    			
    			Robot.clawPID.wheelOut();
    			
    			try {
    				TimeUnit.SECONDS.sleep(2);
    			} catch (InterruptedException e) {
    				// TODO Auto-generated catch block
    				e.printStackTrace();
    			}
    			
    			Robot.clawPID.clawOpen();
    			
    		}
    			
    		if (gameData.charAt(1) == 'R') {
    			
    		}
    		
    	}
    	
    }

    // Make this return true when this Command no longer needs to run execute()
    @Override
    protected boolean isFinished() {
        return true;
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
