// --------------------------------------------------------------------
// MqttMsg.java -- Class to contain Mqtt Messages, with age data.
//
// Created 3/19/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

//import java.io.*;
//import java.util.ArrayList;
//import java.util.concurrent.locks.*;
import java.util.Date;

// Class to contain a Mqtt Message object that is
// received from the network (i.e., from the broker on
// the network.
public class MqttMsg {
	private String m_topic;
	private String m_message;
	private long m_timestamp;
	
	public MqttMsg(String topic, String msg)
	{
		m_topic = topic;
		m_message = msg;
		m_timestamp = StopWatch.timestamp();
	}
	
	// Gets the topic of the message.
	public String getTopic() {
		return m_topic;
	}
	
	// Gets the content of the message.
	public String getMessage() {
		return m_message;
	}
	
	// Returns the timestamp that is assigned to the message
	// when it is received from MQTT at the RoboRio.
	public long getTimestamp() {
		return m_timestamp;
	}
	
	// Returns the age of the message in milliseconds.  The age is 
	// calculate from the time it is received into the RoboRio.
	public long getAge() {
		return StopWatch.stop(m_timestamp);
	}
	
	// Attempts to return the payload as a double.  On fail, returns 0.0.
	public double getDouble() {
		double f;
		try {
			f = Double.parseDouble(m_message.trim());
		}
		catch (NumberFormatException ee) {
			return 0.0;
		}
		catch (NullPointerException ee) {
			return 0.0;
		}
		return f;
	}
	
	// Attempts to return the payload as a long integer.  On fail, returns 0.
	public long getLong() {
		long i;
		try {
			i = Long.parseLong(m_message.trim());
		}
		catch (NumberFormatException ee) {
			return 0;
		}
		catch (NullPointerException ee) {
			return 0;
		}
		return i;
	}
	
	// Gets the content of the message as a "payload" of bytes.
	public byte[] getPayload() {
		return m_message.getBytes();
	}
}