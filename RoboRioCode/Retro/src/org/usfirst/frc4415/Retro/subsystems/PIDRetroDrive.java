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
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj.RobotBase;
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
    
    public boolean toggleDrive; //true equals arcade drive, false equals mecanum drive
    
    public float totalTicks = 0;
    public double totalError = 0;
    public double prevError = 0;
    public long prevTicks = 0;

    // Initialize your subsystem here
    public PIDRetroDrive() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=PID

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=PID
    	
    	super("PIDRetroDrive", -.005, -0.01, 0);
        setAbsoluteTolerance(0.2);
        getPIDController().setContinuous(false);
        LiveWindow.addActuator("PID RetroDrive", "PIDSubsystem Controller", getPIDController());
        
        System.out.println(this.quadratureEncoder1.getDistance());

        // Use these to get going:
        // setSetpoint() -  Sets where the PID controller should move the system
        //                  to
        // enable() - Enables the PID controller.
        
        //setSetpoint(1000);
        //enable();
    }
    
    @Override
    public void enable() {
      super.enable();
      
      prevTicks = System.currentTimeMillis();
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

      
    	return this.quadratureEncoder1.getDistance();
    }

    @Override
    protected void usePIDOutput(double output) {
        // Use output to drive your system, like a motor
        // e.g. yourMotor.set(output);
    	
    	double changeInError = (this.getPIDController().getError() - prevError) / (System.currentTimeMillis() - prevTicks);
    	
    	totalError = totalError + this.getPIDController().getError();
    	totalError = totalError * 0.99;
    	
    	//System.out.println("ERRROR " + String.valueOf(totalError));
    	
    	
    	double newOutput = this.getPIDController().getError() * this.getPIDController().getP() + totalError * this.getPIDController().getI() + changeInError * this.getPIDController().getD();
    	newOutput = clamp(newOutput, -1, 1);
    	
        leftRear.pidWrite(newOutput);
        rightFront.pidWrite(newOutput);
		leftRear.pidWrite(newOutput);
		rightRear.pidWrite(newOutput);
		
        prevError = this.getPIDController().getError();
 
        prevTicks = System.currentTimeMillis();
        
        output = newOutput;

        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=OUTPUT
        leftRear.pidWrite(output);

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=OUTPUT
        
        
        System.out.println(quadratureEncoder1.getDistance());
        
        //System.out.println(this.getPIDController().getError());
        //System.out.println(this.getPIDController().onTarget());
        //long bigTime = (System.currentTimeMillis() - prevTicks);
        
    }
    
    /*public void PIDLoop(double setpoint) {
    	
    	quadratureEncoder1.reset();
    	
    	boolean onPoint = false;
    	
    	super.enable();
        prevTicks = System.currentTimeMillis();
        
        setpoint = setpoint * 3.7685;
        double error = 0;
        error = setpoint - this.returnPIDInput();
        
        double thresholdLeft = 0;
        thresholdLeft = setpoint * .95;
        
        double thresholdRight = 0;
        thresholdRight = setpoint + (setpoint * .05);
        
        if (onPoint == false) {
        	double changeInError = (error - prevError) / (System.currentTimeMillis() - prevTicks);
        	
        	totalError = totalError + error;
        	totalError = totalError * 0.99;
        	
        	//System.out.println("ERRROR " + String.valueOf(totalError));
        	
        	double output = error * this.getPIDController().getP() + totalError * this.getPIDController().getI() + changeInError * this.getPIDController().getD();
        	output = clamp(output, -1, 1);
        	
            leftRear.set(output);
            rightFront.set(output);
    		leftRear.set(output);
    		rightRear.set(output);
    		
            prevError = error;
     
            prevTicks = System.currentTimeMillis();
            
         
            System.out.println(quadratureEncoder1.getDistance());
            
            if (thresholdLeft < Math.abs(quadratureEncoder1.get()) && thresholdRight > Math.abs(quadratureEncoder1.get())) {
            	onPoint = true;
            } else {
            	onPoint = false;
            }
            
            //System.out.println(this.getPIDController().getError());
            //System.out.println(this.getPIDController().onTarget());
            //long bigTime = (System.currentTimeMillis() - prevTicks);
            
        }
        
        
    }*/
    
    
    public void PIDMove(double setpoint) {
    	setSetpoint(setpoint);
    	
    }
    
    public void MecanumDrive() {
    	RobotMap.pIDRetroDriveleftFront.setInverted(true); //change to true for Retro - Steamworks
    	RobotMap.pIDRetroDriveleftRear.setInverted(true);
    	RobotMap.pIDRetroDriverightFront.setInverted(false); // change to false for Retro - Steamworks
    	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	robotDrive4.mecanumDrive_Cartesian(Robot.oi.getRetroStick().getRawAxis(0), Robot.oi.getRetroStick().getRawAxis(1), Robot.oi.getRetroStick().getRawAxis(4), 0);
    }
    
    public void ArcadeDrive() {
    	RobotMap.pIDRetroDriveleftFront.setInverted(false); //change to false for Retro - Steamworks
    	RobotMap.pIDRetroDriveleftRear.setInverted(false);
    	RobotMap.pIDRetroDriverightFront.setInverted(false); //change to false for Retro - Steamworks
    	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	robotDrive4.arcadeDrive(Robot.oi.getRetroStick().getRawAxis(1), Robot.oi.getRetroStick().getRawAxis(4));
    }
    
    public void motorsOff() {
    	leftFront.set(0);
		rightFront.set(0);
		leftRear.set(0);
		rightRear.set(0);
    }
    
    public void toggleDrive() {
    	toggleDrive = !toggleDrive;
    	
    	if (toggleDrive == true) {
    		doubleSolenoid1.set(DoubleSolenoid.Value.kReverse);
    	} else if (toggleDrive == false) {
    		doubleSolenoid1.set(DoubleSolenoid.Value.kForward);
    	}
    }
    
    public void driveForwardDistance(double distance, double startSlowSpeed, double speed1, double speed2, boolean resetEncoder) {  // in cm    	
    	if (toggleDrive == false) {
    		RobotMap.pIDRetroDriveleftFront.setInverted(false);
        	RobotMap.pIDRetroDriveleftRear.setInverted(false);
        	RobotMap.pIDRetroDriverightFront.setInverted(false);
        	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	}
    	
    	double setpoint;
    	setpoint = distance * 3.7302787;
    	quadratureEncoder1.reset();
    	
    	while (quadratureEncoder1.get() < (setpoint * startSlowSpeed)) {
    		leftFront.set(-1 * speed1);
    		rightFront.set(speed1);
    		leftRear.set(-1 * speed1);
    		rightRear.set(speed1);
    		
    		}
    		
    		while (quadratureEncoder1.get() < setpoint) {
        		leftFront.set(-1 * speed2);
        		rightFront.set(speed2);
        		leftRear.set(-1 * speed2);
        		rightRear.set(speed2);
    		}
    	
    	if (resetEncoder == true) {
    		quadratureEncoder1.reset();
    	}
    	
    }
    
    public void driveBackwardDistance(double distance, double startSlowSpeed, double speed1, double speed2, boolean resetEncoder) {  // in cm
    	if (toggleDrive == false) {
    		RobotMap.pIDRetroDriveleftFront.setInverted(false);
        	RobotMap.pIDRetroDriveleftRear.setInverted(false);
        	RobotMap.pIDRetroDriverightFront.setInverted(false);
        	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	}
    	
    	double setpoint;
    	setpoint = distance * 3.7302787;
    	quadratureEncoder1.reset();
    	
    	while (Math.abs(quadratureEncoder1.get()) < (setpoint * startSlowSpeed)) {
    		leftFront.set(speed1);
    		rightFront.set(-1 *speed1);
    		leftRear.set(speed1);
    		rightRear.set(-1 * speed1);
    		}
    		
    		while (Math.abs(quadratureEncoder1.get()) < setpoint) {
        		leftFront.set(speed2);
        		rightFront.set(-1 * speed2);
        		leftRear.set(speed2);
        		rightRear.set(-1 * speed2);
    		}
    	
    	if (resetEncoder == true) {
    		quadratureEncoder1.reset();
    	}
    	
    }
    
    public void turnRightAngle(double angle, double startSlowSpeed, double speed1, double speed2, boolean resetGyro) {  // in cm
    	if (toggleDrive == false) {
    		RobotMap.pIDRetroDriveleftFront.setInverted(false);
        	RobotMap.pIDRetroDriveleftRear.setInverted(false);
        	RobotMap.pIDRetroDriverightFront.setInverted(false);
        	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	}
    	
    	Robot.navX.reset();
    	
    	while (Robot.navX.getAngle() < (angle * startSlowSpeed)) {
    		leftFront.set(-1 * speed1);
    		rightFront.set(-1 * speed1);
    		leftRear.set(-1 * speed1);
    		rightRear.set(-1 * speed1);
    		}
    		
    		while (Robot.navX.getAngle() < angle) {
        		leftFront.set(-1 * speed2);
        		rightFront.set(-1 * speed2);
        		leftRear.set(-1 * speed2);
        		rightRear.set(-1 * speed2);
    		}
    	
    	if (resetGyro == true) {
    		Robot.navX.reset();
    	}
    	
    }
    	
    
    public void turnLeftAngle(double angle, double startSlowSpeed, double speed1, double speed2, boolean resetGyro) {  // in cm
    	if (toggleDrive == false) {
    		RobotMap.pIDRetroDriveleftFront.setInverted(false);
        	RobotMap.pIDRetroDriveleftRear.setInverted(false);
        	RobotMap.pIDRetroDriverightFront.setInverted(false);
        	RobotMap.pIDRetroDriverightRear.setInverted(false);
    	}
    	
    	Robot.navX.reset();
    	
    	while (Math.abs(Robot.navX.getAngle()) < (angle * startSlowSpeed)) {
    		leftFront.set(speed1);
    		rightFront.set(speed1);
    		leftRear.set(speed1);
    		rightRear.set(speed1);
    		if (Robot.navX.getAngle() > angle * startSlowSpeed) {
    			break;
    		}
    		
    		while (Math.abs(Robot.navX.getAngle()) < angle) {
        		leftFront.set(speed2);
        		rightFront.set(speed2);
        		leftRear.set(speed2);
        		rightRear.set(speed2);
    		}
    	
    	}
    	
    	if (resetGyro == true) {
    		Robot.navX.reset();
    	}
    	
    }
    
    public int getEncoder() {
    	return quadratureEncoder1.get();
    }
    
    public void resetEncoder() {
    	quadratureEncoder1.reset();
    }
    
    private static double clamp(double value, double low, double high) {
        return Math.max(low, Math.min(value, high));
      }
    
}
