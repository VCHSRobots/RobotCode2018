// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.PIDRetro.subsystems;

import org.usfirst.frc4415.PIDRetro.Robot;
import org.usfirst.frc4415.PIDRetro.RobotMap;
import org.usfirst.frc4415.PIDRetro.commands.*;
import edu.wpi.first.wpilibj.command.PIDSubsystem;
import edu.wpi.first.wpilibj.livewindow.LiveWindow;
// BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS
import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;
import edu.wpi.first.wpilibj.CounterBase.EncodingType;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.PIDSourceType;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS

/**
 *
 */
public class ClimberPID extends PIDSubsystem {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS
	

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    private final WPI_TalonSRX climberMotor1 = RobotMap.climberPIDclimberMotor1;
    private final WPI_TalonSRX climberMotor2 = RobotMap.climberPIDclimberMotor2;
    private final Encoder quadratureEncoder1 = RobotMap.climberPIDQuadratureEncoder1;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    
    public boolean PIDEnabled = false;
    
    private float totalTicks = 0;
    private double totalError = 0;
    private double prevError = 0;
    public long prevTicks = 0;


    // Initialize your subsystem here
    public ClimberPID() {
        
        super("ClimberPID", 1.0, 0.0, 0.0);
        setAbsoluteTolerance(0.2);
        getPIDController().setContinuous(false);
        LiveWindow.addActuator("ClimberPID", "PIDSubsystem Controller", getPIDController());


        // Use these to get going:
        // setSetpoint() -  Sets where the PID controller should move the system
        //                  to
        // enable() - Enables the PID controller.
    }

    @Override
    public void initDefaultCommand() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        setDefaultCommand(new ClimberDefault());

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        // Set the default command for a subsystem here.
        //setDefaultCommand(new MySpecialCommand());
    }

    @Override
    protected double returnPIDInput() {
        // Return your input value for the PID loop
        // e.g. a sensor, like a potentiometer:
        // yourPot.getAverageVoltage() / kYourMaxVoltage;

        return quadratureEncoder1.getDistance();

    }

    @Override
    protected void usePIDOutput(double output) {
        // Use output to drive your system, like a motor
        // e.g. yourMotor.set(output);

    	
    	double changeInError = (this.getPIDController().getError() - prevError) / (System.currentTimeMillis() - prevTicks);
    	
    	totalError = totalError + this.getPIDController().getError();
    	totalError = totalError * 0.99;
    	
    	double newOutput = this.getPIDController().getError() * this.getPIDController().getP() + totalError * this.getPIDController().getI() + changeInError * this.getPIDController().getD();
    	newOutput = clamp(newOutput, -1, 1);
		
        prevError = this.getPIDController().getError();
 
        prevTicks = System.currentTimeMillis();
        
        newOutput = output;
        output = .5 * output;
        
        System.out.println("Voltage " + output);
        System.out.println("Encoder Value     " + quadratureEncoder1.get());
        System.out.println("PIDEnabled " + PIDEnabled);

        
        climberMotor1.pidWrite(output);
        climberMotor2.pidWrite(output);

    }
    
    private double clamp(double newOutput, int i, int j) {
		// TODO Auto-generated method stub
		return 0;
	}
    
    public void climbUp() {
    	climberMotor1.set(1);
    	climberMotor2.set(1);
    }
    
    public void climbDown() {
    	climberMotor1.set(-1);
    	climberMotor2.set(-1);
    }

	public void climbUpAxis() {
		if (Robot.oi.getManipulatorJoystick().getRawAxis(5) < -.35) {
			climberMotor1.set(1);
	    	climberMotor2.set(1);
		}
    	
    }
    
    public void climbDownAxis() {
    	if (Robot.oi.getManipulatorJoystick().getRawAxis(5) > .35) {
    		climberMotor1.set(-1);
        	climberMotor2.set(-1);
    	}
    	
    }
    
    public void climbOff() {
    	climberMotor1.set(0);
    	climberMotor2.set(0);
    }
    
}
