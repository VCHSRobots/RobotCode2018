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

// BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=IMPORTS
import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;
import edu.wpi.first.wpilibj.CounterBase.EncodingType;
import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.PIDSourceType;
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
    public static WPI_TalonSRX pIDRetroDriveleftFront;
    public static WPI_TalonSRX pIDRetroDriverightFront;
    public static WPI_TalonSRX pIDRetroDriveleftRear;
    public static WPI_TalonSRX pIDRetroDriverightRear;
    public static RobotDrive pIDRetroDriveRobotDrive4;
    public static Encoder pIDRetroDriveQuadratureEncoder1;
    public static DoubleSolenoid pIDRetroDriveDoubleSolenoid1;
    public static WPI_TalonSRX pIDRetroClimberMotor;
    public static Encoder pIDRetroClimberQuadratureEncoder1;

    // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=DECLARATIONS

    public static void init() {
        // BEGIN AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTORS
        pIDRetroDriveleftFront = new WPI_TalonSRX(7);
        
        
        pIDRetroDriverightFront = new WPI_TalonSRX(2);
        
        
        pIDRetroDriveleftRear = new WPI_TalonSRX(6);
        
        
        pIDRetroDriverightRear = new WPI_TalonSRX(3);
        
        
        pIDRetroDriveRobotDrive4 = new RobotDrive(pIDRetroDriveleftFront, pIDRetroDriveleftRear,
              pIDRetroDriverightFront, pIDRetroDriverightRear);
        
        pIDRetroDriveRobotDrive4.setSafetyEnabled(true);
        pIDRetroDriveRobotDrive4.setExpiration(0.1);
        pIDRetroDriveRobotDrive4.setSensitivity(0.5);
        pIDRetroDriveRobotDrive4.setMaxOutput(1.0);

        pIDRetroDriveQuadratureEncoder1 = new Encoder(1, 2, false, EncodingType.k4X);
        LiveWindow.addSensor("PIDRetroDrive", "Quadrature Encoder 1", pIDRetroDriveQuadratureEncoder1);
        pIDRetroDriveQuadratureEncoder1.setDistancePerPulse(1.0);
        pIDRetroDriveQuadratureEncoder1.setPIDSourceType(PIDSourceType.kRate);
        pIDRetroDriveDoubleSolenoid1 = new DoubleSolenoid(0, 0, 1);
        LiveWindow.addActuator("PIDRetroDrive", "Double Solenoid 1", pIDRetroDriveDoubleSolenoid1);
        
        pIDRetroClimberMotor = new WPI_TalonSRX(0);
        
        
        pIDRetroClimberQuadratureEncoder1 = new Encoder(0, 3, false, EncodingType.k4X);
        LiveWindow.addSensor("PIDRetroClimber", "Quadrature Encoder 1", pIDRetroClimberQuadratureEncoder1);
        pIDRetroClimberQuadratureEncoder1.setDistancePerPulse(1.0);
        pIDRetroClimberQuadratureEncoder1.setPIDSourceType(PIDSourceType.kRate);

        // END AUTOGENERATED CODE, SOURCE=ROBOTBUILDER ID=CONSTRUCTORS
    }
    
}
