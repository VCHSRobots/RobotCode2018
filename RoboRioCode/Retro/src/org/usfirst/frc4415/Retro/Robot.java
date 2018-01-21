// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.Retro;

import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.SPI;
import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.command.Scheduler;
import edu.wpi.first.wpilibj.livewindow.LiveWindow;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.usfirst.frc4415.Retro.commands.*;
import org.usfirst.frc4415.Retro.subsystems.*;

import com.kauailabs.navx.frc.AHRS;

/**
 * The VM is configured to automatically run this class, and to call the
 * functions corresponding to each mode, as described in the TimedRobot
 * documentation. If you change the name of this class or the package after
 * creating this project, you must also update the build.properties file in 
 * the project.
 */
public class Robot extends TimedRobot {

    Command autonomousCommand;
    SendableChooser<Command> chooser = new SendableChooser<>();

    public static OI oi;
    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    public static PIDRetroDrive pIDRetroDrive;
    public static PIDRetroClimber pIDRetroClimber;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    
    public String gameData;
    public static AHRS navX;

    /**
     * This function is run when the robot is first started up and should be
     * used for any initialization code.
     */
    @Override
    public void robotInit() {
        RobotMap.init();
        
        try {
        	navX = new AHRS(SPI.Port.kMXP);
        	navX.reset();	
        } catch (RuntimeException ex ) {
        	DriverStation.reportError("Error instantiating navX MXP:   " + ex.getMessage(), true);
        	navX = null;
        }
        
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTORS
        pIDRetroDrive = new PIDRetroDrive();
        pIDRetroClimber = new PIDRetroClimber();

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTORS
        // OI must be constructed after subsystems. If the OI creates Commands
        //(which it very likely will), subsystems are not guaranteed to be
        // constructed yet. Thus, their requires() statements may grab null
        // pointers. Bad news. Don't move it.
        oi = new OI();

        // Add commands to Autonomous Sendable Chooser
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=AUTONOMOUS

        chooser.addObject("Autonomous Command", new AutonomousCommand());
        chooser.addObject("Auto Switch", new AutoSwitch());
        chooser.addDefault("Autonomous Command", new AutonomousCommand());

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=AUTONOMOUS
        SmartDashboard.putData("Auto mode", chooser);
    }

    /**
     * This function is called when the disabled button is hit.
     * You can use it to reset subsystems before shutting down.
     */
    @Override
    public void disabledInit(){
    	
    	gameData = DriverStation.getInstance().getGameSpecificMessage();
    	SmartDashboard.putString("Disable GameData: ", gameData);

    }

    @Override
    public void disabledPeriodic() {
        Scheduler.getInstance().run();
    }

    @Override
    public void autonomousInit() {
        autonomousCommand = chooser.getSelected();
        // schedule the autonomous command (example)
        if (autonomousCommand != null) autonomousCommand.start();
        
        gameData = DriverStation.getInstance().getGameSpecificMessage();
    	SmartDashboard.putString("Auto GameData: ", gameData);
    	
        Robot.pIDRetroDrive.resetEncoder();
        
    }

    /**
     * This function is called periodically during autonomous
     */
    @Override
    public void autonomousPeriodic() {
        Scheduler.getInstance().run();
        
        SmartDashboard.putNumber("Auto Encoder Value: ", Robot.pIDRetroDrive.getEncoder());
        SmartDashboard.putNumber("Auto Distance Value: ", Robot.pIDRetroDrive.getEncoder() / 3.7302787);
        
        
        
    }

    @Override
    public void teleopInit() {
        // This makes sure that the autonomous stops running when
        // teleop starts running. If you want the autonomous to
        // continue until interrupted by another command, remove
        // this line or comment it out.
        if (autonomousCommand != null) autonomousCommand.cancel();
        
        Robot.pIDRetroDrive.resetEncoder();
        
    }

    /**
     * This function is called periodically during operator control
     */
    @Override
    public void teleopPeriodic() {
        Scheduler.getInstance().run();
        
        SmartDashboard.putNumber("Teleop Encoder Value: ", Robot.pIDRetroDrive.getEncoder());
    	SmartDashboard.putNumber("Teleop Distance Value: ", Robot.pIDRetroDrive.getEncoder() / 3.7302787);
        
        
        
    }
}
