// RobotBuilder Version: 2.0
//
// This file was generated by RobotBuilder. It contains sections of
// code that are automatically generated and assigned by robotbuilder.
// These sections will be updated in the future when you export to
// Java from RobotBuilder. Do not put any code or make any change in
// the blocks indicating autogenerated code or it will be lost on an
// update. Deleting the comments indicating the section will prevent
// it from being updated in the future.


package org.usfirst.frc4415.RetroFinal;

// BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS
import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;
import edu.wpi.first.wpilibj.CounterBase.EncodingType;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.PIDSourceType;
import edu.wpi.first.wpilibj.RobotBase;
import edu.wpi.first.wpilibj.RobotDrive;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS
import edu.wpi.first.wpilibj.livewindow.LiveWindow;

/**
 * The RobotMap is a mapping from the ports sensors and actuators are wired into
 * to a variable name. This provides flexibility changing wiring, makes checking
 * the wiring easier and significantly reduces the number of magic numbers
 * floating around.
 */
public class RobotMap {
    // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    public static WPI_TalonSRX driveTrainPIDleftFront;
    public static WPI_TalonSRX driveTrainPIDrightFront;
    public static WPI_TalonSRX driveTrainPIDleftRear;
    public static WPI_TalonSRX driveTrainPIDrightRear;
    public static RobotDrive driveTrainPIDRobotDrive4;
    public static Encoder driveTrainPIDQuadratureEncoder1;
    public static Encoder driveTrainPIDQuadratureEncoder2;
    public static WPI_TalonSRX clawPIDwristMotor;
    public static WPI_TalonSRX clawPIDwheelMotor;
    public static Encoder clawPIDQuadratureEncoder1;
    public static DoubleSolenoid clawPIDDoubleSolenoid1;
    public static DigitalInput clawPIDLimitSwitch1;
    public static WPI_TalonSRX wedgeArmPIDwedgeArmMotor;
    public static Encoder wedgeArmPIDQuadratureEncoder1;
    public static DigitalInput wedgeArmPIDLimitSwitch1;
    public static WPI_TalonSRX climberclimberMotor1;
    public static WPI_TalonSRX climberclimberMotor2;
    public static DoubleSolenoid climberDoubleSolenoid1;
    public static WPI_TalonSRX telescopePIDtelescopeMotor;
    public static Encoder telescopePIDQuadratureEncoder1;
    public static DigitalInput telescopePIDLimitSwitch1;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS
    
    public static WPI_TalonSRX telescopePIDtelescopeMotor2;
    public static WPI_TalonSRX clawPIDwheelMotor2;

    public static void init() {
    	
    	
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTORS
        driveTrainPIDleftFront = new WPI_TalonSRX(3);
        
        
        driveTrainPIDrightFront = new WPI_TalonSRX(4);
        
        
        driveTrainPIDleftRear = new WPI_TalonSRX(5);
        
        
        driveTrainPIDrightRear = new WPI_TalonSRX(6);
        
        
        driveTrainPIDRobotDrive4 = new RobotDrive(driveTrainPIDleftFront, driveTrainPIDleftRear,
              driveTrainPIDrightFront, driveTrainPIDrightRear);
        
        driveTrainPIDRobotDrive4.setSafetyEnabled(false);
        driveTrainPIDRobotDrive4.setExpiration(0.1);
        driveTrainPIDRobotDrive4.setSensitivity(0.5);
        driveTrainPIDRobotDrive4.setMaxOutput(1.0);

        driveTrainPIDQuadratureEncoder1 = new Encoder(10, 11, false, EncodingType.k4X);
        LiveWindow.addSensor("DriveTrainPID", "Quadrature Encoder 1", driveTrainPIDQuadratureEncoder1);
        driveTrainPIDQuadratureEncoder1.setDistancePerPulse(1.0);
        driveTrainPIDQuadratureEncoder1.setPIDSourceType(PIDSourceType.kRate);
        driveTrainPIDQuadratureEncoder2 = new Encoder(12, 13, false, EncodingType.k4X);
        LiveWindow.addSensor("DriveTrainPID", "Quadrature Encoder 2", driveTrainPIDQuadratureEncoder2);
        driveTrainPIDQuadratureEncoder2.setDistancePerPulse(1.0);
        driveTrainPIDQuadratureEncoder2.setPIDSourceType(PIDSourceType.kRate);
        clawPIDwristMotor = new WPI_TalonSRX(7);
         
        
        clawPIDwheelMotor = new WPI_TalonSRX(8);
        clawPIDwheelMotor2 = new WPI_TalonSRX(9);
        
        
        clawPIDQuadratureEncoder1 = new Encoder(4, 5, false, EncodingType.k4X);
        LiveWindow.addSensor("ClawPID", "Quadrature Encoder 1", clawPIDQuadratureEncoder1);
        clawPIDQuadratureEncoder1.setDistancePerPulse(1.0);
        clawPIDQuadratureEncoder1.setPIDSourceType(PIDSourceType.kRate);
        clawPIDDoubleSolenoid1 = new DoubleSolenoid(0, 0, 1);
        LiveWindow.addActuator("ClawPID", "Double Solenoid 1", clawPIDDoubleSolenoid1);
        
        clawPIDLimitSwitch1 = new DigitalInput(8);
        LiveWindow.addSensor("ClawPID", "Limit Switch 1", clawPIDLimitSwitch1);
        
        wedgeArmPIDwedgeArmMotor = new WPI_TalonSRX(2);
        
        
        wedgeArmPIDQuadratureEncoder1 = new Encoder(2, 3, false, EncodingType.k4X);
        LiveWindow.addSensor("WedgeArmPID", "Quadrature Encoder 1", wedgeArmPIDQuadratureEncoder1);
        wedgeArmPIDQuadratureEncoder1.setDistancePerPulse(1.0);
        wedgeArmPIDQuadratureEncoder1.setPIDSourceType(PIDSourceType.kRate);
        wedgeArmPIDLimitSwitch1 = new DigitalInput(9);
        LiveWindow.addSensor("WedgeArmPID", "Limit Switch 1", wedgeArmPIDLimitSwitch1);
        
        climberclimberMotor1 = new WPI_TalonSRX(0);
        
        
        climberclimberMotor2 = new WPI_TalonSRX(1);
        
        
        climberDoubleSolenoid1 = new DoubleSolenoid(0, 2, 3);
        LiveWindow.addActuator("Climber", "Double Solenoid 1", climberDoubleSolenoid1);
        
        telescopePIDtelescopeMotor = new WPI_TalonSRX(11);
        telescopePIDtelescopeMotor2 = new WPI_TalonSRX(12);
        
        telescopePIDQuadratureEncoder1 = new Encoder(0, 1, false, EncodingType.k4X);
        LiveWindow.addSensor("TelescopePID", "Quadrature Encoder 1", telescopePIDQuadratureEncoder1);
        telescopePIDQuadratureEncoder1.setDistancePerPulse(1.0);
        telescopePIDQuadratureEncoder1.setPIDSourceType(PIDSourceType.kRate);
        telescopePIDLimitSwitch1 = new DigitalInput(6);
        LiveWindow.addSensor("TelescopePID", "Limit Switch 1", telescopePIDLimitSwitch1);
        
        
        

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTORS
        
        telescopePIDtelescopeMotor.setInverted(true);
        telescopePIDtelescopeMotor2.setInverted(true);
        clawPIDwheelMotor.setInverted(true);
        clawPIDwheelMotor2.setInverted(true);
        climberclimberMotor1.setInverted(true);
        climberclimberMotor2.setInverted(true);
    }
    
}