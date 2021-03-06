// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.Steam.subsystems;

import org.usfirst.frc4415.Steam.RobotMap;
import org.usfirst.frc4415.Steam.commands.*;
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
public class PIDSub2 extends PIDSubsystem {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    private final WPI_TalonSRX climberMotor = RobotMap.pIDSub2climberMotor;
    private final Encoder quadratureEncoder1 = RobotMap.pIDSub2QuadratureEncoder1;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    public boolean PIDEnabled = false;
    
    private float totalTicks = 0;
    private double totalError = 0;
    private double prevError = 0;
    public long prevTicks = 0;

    // Initialize your subsystem here
    public PIDSub2() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=PID
        super("PIDSub2", 1.0, 0.0, 0.0);
        setAbsoluteTolerance(0.2);
        getPIDController().setContinuous(false);
        LiveWindow.addActuator("PID Sub2", "PIDSubsystem Controller", getPIDController());

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=PID

        // Use these to get going:
        // setSetpoint() -  Sets where the PID controller should move the system
        //                  to
        // enable() - Enables the PID controller.
    }
    
    @Override
    public void enable() {
      super.enable();
      
      PIDEnabled = true;
      prevTicks = System.currentTimeMillis();
    }
    
    @Override
    public void disable() {
    	super.disable();
    	
    	PIDEnabled = false;
    }

    @Override
    public void initDefaultCommand() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        setDefaultCommand(new PIDSubClimber());

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
    	
    	//System.out.println("ERRROR " + String.valueOf(totalError));
    	
    	
    	double newOutput = this.getPIDController().getError() * this.getPIDController().getP() + totalError * this.getPIDController().getI() + changeInError * this.getPIDController().getD();
    	newOutput = clamp(newOutput, -1, 1);
    	
        /*leftRear.pidWrite(newOutput);
        rightFront.pidWrite(newOutput);
		leftRear.pidWrite(newOutput);
		rightRear.pidWrite(newOutput);*/
		
        prevError = this.getPIDController().getError();
 
        prevTicks = System.currentTimeMillis();
        
        newOutput = output;
        output = 1 * output;
        
        //climberMotor.pidWrite(output);
        
        /*System.out.println("Voltage " + output);
        System.out.println("Encoder Value         " + quadratureEncoder1.get());
        System.out.println("PIDEnabled " + PIDEnabled);*/
        System.out.println("PIDSub2.PIDController");
       
    }

	private double clamp(double newOutput, int i, int j) {
		// TODO Auto-generated method stub
		return 0;
	}
}
