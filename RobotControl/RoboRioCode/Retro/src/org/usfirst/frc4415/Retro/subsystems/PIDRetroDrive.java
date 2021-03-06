// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.Retro.subsystems;

import org.usfirst.frc4415.Retro.Robot;
import org.usfirst.frc4415.Retro.RobotMap;
import org.usfirst.frc4415.Retro.commands.*;
import edu.wpi.first.wpilibj.command.PIDSubsystem;
import edu.wpi.first.wpilibj.livewindow.LiveWindow;
// BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS
import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;
import edu.wpi.first.wpilibj.CounterBase.EncodingType;
import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.PIDSourceType;
import edu.wpi.first.wpilibj.RobotDrive;

// END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS

/**
 *
 */
public class PIDRetroDrive extends PIDSubsystem {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    private final WPI_TalonSRX leftFront = RobotMap.pIDRetroDriveleftFront;
    private final WPI_TalonSRX rightFront = RobotMap.pIDRetroDriverightFront;
    private final WPI_TalonSRX leftRear = RobotMap.pIDRetroDriveleftRear;
    private final WPI_TalonSRX rightRear = RobotMap.pIDRetroDriverightRear;
    private final RobotDrive robotDrive4 = RobotMap.pIDRetroDriveRobotDrive4;
    private final Encoder quadratureEncoder1 = RobotMap.pIDRetroDriveQuadratureEncoder1;
    private final DoubleSolenoid doubleSolenoid1 = RobotMap.pIDRetroDriveDoubleSolenoid1;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    
    public boolean toggleDrive = true; //true equals arcade drive, false equals mecanum drive

    // Initialize your subsystem here
    public PIDRetroDrive() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=PID
        super("PIDRetroDrive", 1.0, 0.0, 0.0);
        setAbsoluteTolerance(0.2);
        getPIDController().setContinuous(false);
        LiveWindow.addActuator("PID RetroDrive", "PIDSubsystem Controller", getPIDController());

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=PID

        // Use these to get going:
        // setSetpoint() -  Sets where the PID controller should move the system
        //                  to
        // enable() - Enables the PID controller.
    }

    @Override
    public void initDefaultCommand() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        setDefaultCommand(new RetroDriveDefault());

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        // Set the default command for a subsystem here.
        //setDefaultCommand(new MySpecialCommand());
    }

    @Override
    protected double returnPIDInput() {
        // Return your input value for the PID loop
        // e.g. a sensor, like a potentiometer:
        // yourPot.getAverageVoltage() / kYourMaxVoltage;

        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=SOURCE
        return quadratureEncoder1.pidGet();

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=SOURCE
    }

    @Override
    protected void usePIDOutput(double output) {
        // Use output to drive your system, like a motor
        // e.g. yourMotor.set(output);

        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=OUTPUT
        leftRear.pidWrite(output);

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=OUTPUT
    }
    
    public void mecanumDrive() {
    	RobotMap.pIDRetroDriveleftFront.setInverted(true);
    	RobotMap.pIDRetroDriveleftRear.setInverted(true);
    	RobotMap.pIDRetroDriverightFront.setInverted(false);
    	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	robotDrive4.mecanumDrive_Cartesian(Robot.oi.getRetroStick().getRawAxis(0), Robot.oi.getRetroStick().getRawAxis(1), Robot.oi.getRetroStick().getRawAxis(4), 0);
    }
    
    public void arcadeDrive() {
    	RobotMap.pIDRetroDriveleftFront.setInverted(false);
    	RobotMap.pIDRetroDriveleftRear.setInverted(false);
    	RobotMap.pIDRetroDriverightFront.setInverted(false);
    	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	robotDrive4.arcadeDrive(Robot.oi.getRetroStick().getRawAxis(1), Robot.oi.getRetroStick().getRawAxis(4));
    }
    
    public void toggleDrive() {
    	toggleDrive = !toggleDrive;
    	
    	if (toggleDrive == true) {
    		doubleSolenoid1.set(DoubleSolenoid.Value.kReverse);
    	} else if (toggleDrive == false) {
    		doubleSolenoid1.set(DoubleSolenoid.Value.kForward);
    	}
    }
    
    // Autonoumous Functions Start Here
    
    public void driveForwardDistance(double distance, double startSlowSpeed, double speed1, double speed2) {  // in cm
    	double setpoint;
    	setpoint = distance * 3.7302787;
    	quadratureEncoder1.reset();
    	while (quadratureEncoder1.get() < setpoint) {
    		leftFront.set(-1 * speed1);
    		rightFront.set(speed1);
    		leftRear.set(-1 * speed1);
    		rightRear.set(speed1);
    		if (quadratureEncoder1.get() > (setpoint * startSlowSpeed)) {
    			break;
    		}
    		
    		while (quadratureEncoder1.get() < setpoint) {
        		leftFront.set(-1 * speed2);
        		rightFront.set(speed2);
        		leftRear.set(-1 * speed2);
        		rightRear.set(speed2);
    		}
    	
    		quadratureEncoder1.reset();
    		
    	}
    	
    }
    
    
    
    public void driveBackwardDistance(double distance, double startSlowSpeed, double speed1, double speed2) {  // in cm
    	double setpoint;
    	setpoint = distance * 3.7302787;
    	quadratureEncoder1.reset();
    	while (quadratureEncoder1.get() > setpoint) {
    		leftFront.set(speed1);
    		rightFront.set(-1 * speed1);
    		leftRear.set(speed1);
    		rightRear.set(-1 * speed1);
    		if (quadratureEncoder1.get() < (setpoint * startSlowSpeed)) {
    			break;
    		}
    		
    		while (quadratureEncoder1.get() > setpoint) {
        		leftFront.set(speed2);
        		rightFront.set(-1 * speed2);
        		leftRear.set(speed2);
        		rightRear.set(-1 * speed2);
    		}
    	
    		quadratureEncoder1.reset();
    		
    	}
    	
    }
    
    public void turnRightAngle(double angle, double startSlowSpeed, double speed1, double speed2, boolean resetGyro) {  // in cm
    	
    	Robot.navX.reset();
    	double currentAngle = Robot.navX.getAngle();
    	
    	while (currentAngle < angle) {
    		leftFront.set(-1 * speed1);
    		rightFront.set(-1 * speed1);
    		leftRear.set(-1 * speed1);
    		rightRear.set(-1 * speed1);
    		if (currentAngle > (angle * startSlowSpeed)) {
    			break;
    		}
    		
    		while (currentAngle < angle) {
        		leftFront.set(-1 * speed2);
        		rightFront.set(-1 * speed2);
        		leftRear.set(-1 * speed2);
        		rightRear.set(-1 * speed2);
    		}
    	
    		if (resetGyro == true) {
    			Robot.navX.reset();
    		}
    		
    	}
    	
    }
    
public void turnLeftAngle(double angle, double startSlowSpeed, double speed1, double speed2) {  // in cm
    	
    	Robot.navX.reset();
    	double currentAngle = Robot.navX.getAngle();
    	
    	while (currentAngle < angle) {
    		leftFront.set(speed1);
    		rightFront.set(speed1);
    		leftRear.set(speed1);
    		rightRear.set(speed1);
    		if (currentAngle > (angle * startSlowSpeed)) {
    			break;
    		}
    		
    		while (currentAngle < angle) {
        		leftFront.set(speed2);
        		rightFront.set(speed2);
        		leftRear.set(speed2);
        		rightRear.set(speed2);
    		}
    	
    	}
    	
    }
    
    public void driveForward(double speed1) {
    	leftFront.set(-1 * speed1);
		rightFront.set(speed1);
		leftRear.set(-1 * speed1);
		rightRear.set(speed1);
    }
    
    public void driveBackward(double speed1) {
    	leftFront.set(speed1);
		rightFront.set(-1 * speed1);
		leftRear.set(speed1);
		rightRear.set(-1 * speed1);
    }
    
    public void turnRight(double speed1) {
    	leftFront.set(-1 * speed1);
		rightFront.set(-1 * speed1);
		leftRear.set(-1 * speed1);
		rightRear.set(-1 * speed1);
    }
    
    public void turnLeft (double speed1) {
    	leftFront.set(speed1);
		rightFront.set(speed1);
		leftRear.set(speed1);
		rightRear.set(speed1);
    }
    
    public void motorsOff() {
    	leftFront.set(0);
		rightFront.set(0);
		leftRear.set(0);
		rightRear.set(0);
    }
    
    public int getEncoder() {
    	return quadratureEncoder1.get();
    }
    
    public void resetEncoder() {
    	quadratureEncoder1.reset();
    }
    
    public double getGyroAngle() {
    	return Robot.navX.getAngle();
    }
    
    public void resetGyroAngle() {
    	Robot.navX.reset();
    }
    
}
