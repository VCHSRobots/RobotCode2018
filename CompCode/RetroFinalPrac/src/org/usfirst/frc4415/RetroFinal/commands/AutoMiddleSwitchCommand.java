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
import org.usfirst.frc4415.RetroFinal.RobotMap;

/**
 *
 */
public class AutoMiddleSwitchCommand extends Command {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
 
    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=VARIABLE_DECLARATIONS
	
	String gameData;
	
	boolean autoDone = false;

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTOR
    public AutoMiddleSwitchCommand() {
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
    		
    		if (gameData.charAt(0) == 'L') {
    			
    			new BoundedWristSetpoint().start();
    			new MyTelescopeSwitchSetpoint().start();
    			new MyWedgeArmSwitchSetpoint().start();
    			new MyWristSwitchSetpoint().start();
    			
    			/*try {
    				TimeUnit.SECONDS.sleep(4);
    			} catch (InterruptedException e) {
    				// TODO Auto-generated catch block
    				e.printStackTrace();
    			}*/
    			
    			while (Robot.navX.getAngle() >= -60) {
    				RobotMap.driveTrainPIDRobotDrive4.drive(1, -.7);
    			}
    			
    			while (Robot.navX.getAngle() <= -8) {
    				RobotMap.driveTrainPIDRobotDrive4.drive(1, .7);
    			}
    			
    			new WheelShootTimed(1).start();
    			
    			new ClawOpen().start();
    			
    			autoDone = true;
    		}
    			
    		if (gameData.charAt(0) == 'R') {
    			
    		}
    		
    	}
    		
    }

    // Make this return true when this Command no longer needs to run execute()
    @Override
    protected boolean isFinished() {
        return autoDone;
    }

    // Called once after isFinished returns true
    @Override
    protected void end() {
    	
    	autoDone = false;
    	
    }

    // Called when another command which requires one or more of the same
    // subsystems is scheduled to run
    @Override
    protected void interrupted() {
    }
}