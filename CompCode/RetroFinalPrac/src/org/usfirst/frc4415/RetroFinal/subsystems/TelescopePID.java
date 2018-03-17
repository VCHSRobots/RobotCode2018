// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.RetroFinal.subsystems;

import org.usfirst.frc4415.RetroFinal.Robot;
import org.usfirst.frc4415.RetroFinal.RobotMap;
import org.usfirst.frc4415.RetroFinal.commands.*;
import edu.wpi.first.wpilibj.command.PIDSubsystem;
import edu.wpi.first.wpilibj.livewindow.LiveWindow;
// BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS
import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;
import edu.wpi.first.wpilibj.CounterBase.EncodingType;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.PIDSourceType;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS

/**
 *
 */
public class TelescopePID extends PIDSubsystem {

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTANTS

    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    private final WPI_TalonSRX telescopeMotor = RobotMap.telescopePIDtelescopeMotor;
    private final Encoder quadratureEncoder1 = RobotMap.telescopePIDQuadratureEncoder1;
    private final DigitalInput limitSwitch1 = RobotMap.telescopePIDLimitSwitch1;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    
    public boolean telescopePIDEnabled = false;
    
    private float totalTicks = 0;
    private double totalError = 0;
    private double prevError = 0;
    public long prevTicks = 0;

    // Initialize your subsystem here
    public TelescopePID() {
        
        super("TelescopePID", -.08, 0.0, 0.0);
        setAbsoluteTolerance(0.2);
        getPIDController().setContinuous(false);
        LiveWindow.addActuator("Telescope PID", "PIDSubsystem Controller", getPIDController());

        // Use these to get going:
        // setSetpoint() -  Sets where the PID controller should move the system
        //                  to
        // enable() - Enables the PID controller.
    }

    @Override
    public void initDefaultCommand() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        setDefaultCommand(new TelescopeDefault());

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DEFAULT_COMMAND

        // Set the default command for a subsystem here.
        //setDefaultCommand(new MySpecialCommand());
    }
    
    @Override
    public void enable() {
      super.enable();
      
      telescopePIDEnabled = true;
      prevTicks = System.currentTimeMillis();
    }
    
    @Override
    public void disable() {
    	super.disable();
    	
    	telescopePIDEnabled = false;
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
        output = 1 * output;
        
        telescopeMotor.pidWrite(output);
        
        System.out.println("Telescope Voltage " + output);
        System.out.println("Telescope Encoder Value " + quadratureEncoder1.get());
        System.out.println("Telescope PIDEnabled " + telescopePIDEnabled);

    }
    
    public void telescopeUp() {
    	telescopeMotor.set(-1);
    }
    
    public void telescopeDown() {
    	telescopeMotor.set(1);
    }
    
    public void telescopeOff() {
    	telescopeMotor.set(0);
    }
    
    public void telescopeUpPOV() {
    	if (Robot.oi.getDriverJoystick().getPOV() == 0) {
    		telescopeMotor.set(-1);
    	}
    }
    
    public void telescopeDownPOV() {
    	if (Robot.oi.getDriverJoystick().getPOV() == 180) {
    		telescopeMotor.set(1);
    	}
    }
    
    public void telescopeUpHalf() {
    	telescopeMotor.set(-.882);
    }
    
    public void telescopeDownHalf() {
    	telescopeMotor.set(.74);
    }
    
    public double getEncoder() {
    	return quadratureEncoder1.get();
    }
    
    public void resetEncoder() {
    	quadratureEncoder1.reset();
    }
    
    public boolean getLimitSwitch1() {
    	return limitSwitch1.get();
    }

	private double clamp(double newOutput, int i, int j) {
		// TODO Auto-generated method stub
		return 0;
	}
}
