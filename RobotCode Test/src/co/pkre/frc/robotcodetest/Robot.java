package co.pkre.frc.robotcodetest;

import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;

import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.PosixFilePermission;
import java.util.EnumSet;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.FeedbackDevice;
import com.ctre.phoenix.motorcontrol.NeutralMode;

import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.IterativeRobot;
import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.RobotController;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

public class Robot extends IterativeRobot
{
	/*
	 * Variables.
	 */
	
	// DriverStation variables.
	
	private DriverStation DS = edu.wpi.first.wpilibj.DriverStation.getInstance();
	private Joystick Controller = new Joystick(0);
	
	// Robot variables.
	
	public static WPI_TalonSRX Spinner = new WPI_TalonSRX(1);
	private double WheelDiameter = 0.2; // Wheel radius in INCHES.
	
	// Program variables.

	private String FileName;
	private boolean Toggle = false;
	
	/*
	 * Functions.
	 */
	
	@Override
	public void autonomousInit()
	{
		// TODO: Do something during autonomous.
	}
	
	@Override
	public void autonomousPeriodic()
	{
		// TODO: Do something during autonomous.
	}
	
	@Override
	public void disabledInit()
	{
		// TODO: Do something during disabled.
	}
	
	@Override
	public void disabledPeriodic()
	{
		Spinner.set(ControlMode.PercentOutput, 0.0);
	}
	
	@Override
	public void robotInit()
	{
		System.out.println("Robot initialized!");
		Spinner.setNeutralMode(NeutralMode.Coast);
		Spinner.configOpenloopRamp(0.25, 1);
		Spinner.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder, 0, 10);
		Spinner.setSensorPhase(true);
		
		String FileName = "C:\\Users\\3265MNE\\Downloads\\Log-" + java.time.Instant.now() + ".csv";
		File LogFile = new File(FileName);
		try
		{
			LogFile.createNewFile();
		}
		catch (IOException e0)
		{
			e0.printStackTrace();
		}
		try
		{
		Files.setPosixFilePermissions(LogFile.toPath(), EnumSet.of(PosixFilePermission.OWNER_READ, PosixFilePermission.OWNER_WRITE, PosixFilePermission.OWNER_EXECUTE, PosixFilePermission.GROUP_READ, PosixFilePermission.GROUP_EXECUTE));
		}
		catch (IOException e3)
		{
			e3.printStackTrace();
		}
		try
		{
			Files.write(Paths.get(FileName), "Battery voltage, Motor ID, Motor speed [RPM], Motor distance, Motor bus voltage, Motor output voltage, Motor output amperage, Motor temperature\r\n".getBytes(), StandardOpenOption.APPEND);
		}
		catch (IOException e1)
		{
			e1.printStackTrace();
		}
	}
	
	@Override
	public void robotPeriodic()
	{
		// TODO: Do something during robotPeriodic.
	}
	
	private static double round(double Value, int Places) // Because Java's default "round()" is terrible!
	{
		if (Places < 0)
		{
			throw new IllegalArgumentException();
		}
		BigDecimal BD = new BigDecimal(Double.toString(Value));
		BD = BD.setScale(Places, RoundingMode.HALF_UP);
		return BD.doubleValue();
	}
	
	@Override
	public void teleopInit()
	{
		// TODO: Do something during Teleoperated Initialization.
	}
	
	@Override
	public void teleopPeriodic()
	{
		UpdateData();
		if (Controller.getRawButton(1)) // When button 1 is pressed, "change gears".
		{
			Spinner.stopMotor();
			Spinner.setSelectedSensorPosition(0, 0, 0);
			if (Toggle == false)
			{
				Toggle = true;
				System.out.println("Initializing PID / MotionPath test.");
				edu.wpi.first.wpilibj.Timer.delay(0.25);
				// TODO: Do PID test.
				edu.wpi.first.wpilibj.Timer.delay(0.25);
				System.out.println("PID / MotionPath test complete.");
				Toggle = false;
			}
		}
		else // Otherwise we drive normally.
		{
			double Value = Controller.getY() * -1.0;
			if (Value == 0)
			{
				Spinner.setSelectedSensorPosition(0, 0, 0);
			}
			Spinner.set(ControlMode.PercentOutput, Value);
		}
	}
	
	@Override
	public void testInit()
	{
		
	}
	
	@Override
	public void testPeriodic()
	{
		
	}
	
	public void UpdateData()
	{
		// Game state data.
		if (DS.isAutonomous())
		{
			SmartDashboard.putString("Current Game State:", "Autonomous.");
		}
		else
		{
			SmartDashboard.putString("Current Game State:", "Teleoperated.");
		}
		if (DS.isTest())
		{
			SmartDashboard.putString("Robot mode:", "Testing.");
		}
		else
		{
			SmartDashboard.putString("Robot mode:", "Live.");
		}
		// Hardware data.
		int MotorID = 1;
		
		double BatteryVoltage = RobotController.getBatteryVoltage();

		double Temperature = Spinner.getTemperature();
		double SpeedRPM = round(Spinner.getSelectedSensorVelocity(0) / 4096.0 * 600.0, 0); // Sensor units per 100 MS. The sensor we are using (Quadrature encoder) has 4096 units per rotation. Speed is converted to RPM.
		double SpeedMPH =  (SpeedRPM * WheelDiameter * Math.PI * 60.0) / 63360.0; // (Circumference * RPM * 60 minutes per hour) / Inches per mile.
		int Position = Spinner.getSelectedSensorPosition(0);
		double BusVoltage = Spinner.getBusVoltage();
		double OutputVoltage = Math.abs(Spinner.getMotorOutputVoltage());
		double OutputAmperage = Spinner.getOutputCurrent();
		
		SmartDashboard.putNumber("Battery voltage:", BatteryVoltage);
		
		SmartDashboard.putNumber("Motor temperature", Temperature);
		SmartDashboard.putNumber("Motor speed (RPM):", SpeedRPM);
		SmartDashboard.putNumber("Motor speed (MPH):", SpeedMPH);
		SmartDashboard.putNumber("Motor distance:", Position);
		SmartDashboard.putNumber("Motor bus voltage:", BusVoltage);
		SmartDashboard.putNumber("Motor output voltage:", OutputVoltage);
		SmartDashboard.putNumber("Motor output amperage", OutputAmperage);
		
		try
		{
			Files.write(Paths.get(FileName), String.format("%s, %s, %s, %s, %s, %s, %s, %s\r\n", BatteryVoltage, MotorID, SpeedRPM, Position, BusVoltage, OutputVoltage, OutputAmperage, Temperature).getBytes(), StandardOpenOption.APPEND);
		}
		catch (IOException e2)
		{
			e2.printStackTrace();
		}
	}
}