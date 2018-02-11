// --------------------------------------------------------------------
// Mqtt.java -- Class to do comm with MQTT in the background.
//
// Created 3/18/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.RoboRioTest;

import org.eclipse.paho.client.mqttv3.MqttClient;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.util.ArrayList;

public class Mqtt extends Thread implements MqttCallback {
	
	private String m_hostName;
	private int m_portNumber;
	private String m_clientId;
	private MqttClient m_client = null;
	private int m_count = 0;
	private Lock m_lockIncoming = new ReentrantLock();
	private Lock m_lockOutgoing = new ReentrantLock();
	private ArrayList<MqttMsg> m_incomingMsgLst;
	private ArrayList<MqttMsg> m_outgoingMsgLst;
	private ArrayList<MqttMsg> m_saveMsgLst;
	private boolean m_restart = false;
	private int m_nCountSent = 0;
	private int m_nCountReceived = 0;
	private int m_nCountErrors = 0;
	private int m_nCountDup = 0;

	public Mqtt(String hostName, int portNumber, String clientId) {
		this.m_hostName = hostName;
		this.m_portNumber = portNumber;
		this.m_clientId = clientId;
		this.setName("MQTT");
		m_incomingMsgLst = new ArrayList<MqttMsg>();
		m_outgoingMsgLst = new ArrayList<MqttMsg>();
		m_saveMsgLst = new ArrayList<MqttMsg>();
	}
	
	// This is the main background thread for mqtt.  It keeps checking to
	// make sure a connection is alive.
	public void run() {
		while(true) {
			while (m_client == null) {
				sleep(100);
				m_client = makeConnection();
			}
			try {
				m_client.subscribe("robot/#");  // Subscribe to everything!!!  Sort it out later.
			}
			catch (MqttException ee) {
				threadMessage("Mqtt: Unable to subscribe to MQTT feed.  Retrying in a little while. (" + ee.getMessage() + ").");
				m_nCountErrors++;
				killClient();
				sleep(100);
				continue;  // Start at the top on the main loop.
			}
			long lastCleanupTime = StopWatch.start();
			while (m_client != null && m_client.isConnected()) {
				sleep(20);
				if (m_restart) {
					m_client = null;
					threadMessage("Mqtt: Restart discovered via flag set.  Doing restart.");
					continue;
				}
				m_lockOutgoing.lock();
				ArrayList<MqttMsg> templist = null;
				if (m_outgoingMsgLst.size() > 0) {
					templist = m_outgoingMsgLst;
					m_outgoingMsgLst = new ArrayList<MqttMsg>();
				}
				m_lockOutgoing.unlock();
				if (templist != null) {	
					for(MqttMsg m : templist) {
						
						try {
							m_client.publish(m.getTopic(), m.getPayload(), 0, false);
							m_nCountSent++;
						}
						catch (MqttException ee) {
							threadMessage("Mqtt: Unable to publish.  Killing and restart.  (Error=" + ee.getMessage() + ").");
							m_nCountErrors++;
							killClient();
							break;
						}
					}
				}
				
				if (StopWatch.stop(lastCleanupTime) > 1000) {
					clearOldMessages(1000);
					lastCleanupTime = StopWatch.start();
				}
				
				// Do a heartbeat output here.  Sort of a Kludge... 
				m_count++;
				if (m_count % 200 == 0) {
					MqttMsg m = new MqttMsg("robot/roborio/heartbeat", String.format("%d",  m_count/200));
					m_lockOutgoing.lock();
					m_outgoingMsgLst.add(m);
					m_lockOutgoing.unlock();
				}
			}
		}
	}
	
	// Trys once to make a connection to the broker.  If works, returns a non-null
	// client.  Otherwise returns null.
	private MqttClient makeConnection() {
		MqttClient client = null;
		try {
			m_restart = false;
			MemoryPersistence persistence = new MemoryPersistence();
			String url = String.format("tcp://%s:%d",  m_hostName, m_portNumber);
	        client = new MqttClient(url, m_clientId, persistence);
	        client.setCallback(this);
	        MqttConnectOptions connOpts = new MqttConnectOptions();
	        connOpts.setCleanSession(true);
	        client.connect(connOpts); 
	        threadMessage("MQTT: connected.");
	        return client;
	      }
		catch (MqttException me) {
	       	threadMessage(String.format("MQTT: Error in Mqtt startup. Reason/msg = %s, %s", me.getReasonCode(), me.getMessage()));
			m_nCountErrors++;
	       	return null;
		}
	}
	
	// Writes a message to the console -- prepending it with the name of the thread
	private void threadMessage(String message){
		String threadName = Thread.currentThread().getName();
		System.out.format("%s: %s%n", threadName, message);
	}
	
	// Does a safe sleep for the given number of milliseconds
	private void sleep(int ms){
		try{
			Thread.sleep(ms);
		} 	catch (InterruptedException e){
			threadMessage("MQTT: Thread interrupted at connection attempt.");
		}
	}

	// Trys to kill the client connection but not report any error if fail.
	private void killClient() {
		if (m_client != null) 
		{
			try {
				m_client.disconnect();
			}
			catch (Exception ee) {
				
			}
			m_client = null;
		}
	}
	
	@Override
	public void connectionLost(Throwable arg0) {
		threadMessage("Mqtt: Connection lost.  Setting flag to start reconnect process.");
		m_restart = true;
	}

	@Override
	public void messageArrived(String topic, MqttMessage mqmsg) throws Exception {
		String msgtext = new String(mqmsg.getPayload(), "US-ASCII");
		MqttMsg msg = new MqttMsg(topic, msgtext);
		ArrayList<MqttMsg> templist= new ArrayList<MqttMsg>();
		
		m_lockIncoming.lock();
		m_nCountReceived++;
		m_incomingMsgLst.add(msg);
		
		// Before adding this one to the "save" list, remove any with the same name.
		for(MqttMsg m: m_saveMsgLst) {
			if (!m.getTopic().equals(topic)) templist.add(m);
			else m_nCountDup++;
		}
		m_saveMsgLst = templist;
		m_saveMsgLst.add(msg);
		m_lockIncoming.unlock();
		//threadMessage("\nMqtt: new msg. Topic=" + msg.getTopic() + "\n");
	}

	// Returns the newest message with the given topic.  All previous messages
	// are discarded (deleted).  If the message doesn't exist, null is returned.
	public MqttMsg getMessageByTopic(String topic) {
		MqttMsg bestMsg = null;
		ArrayList<MqttMsg> keepList = new ArrayList<MqttMsg>();
		
		m_lockIncoming.lock();
		for (MqttMsg m: m_incomingMsgLst) {
			if (m.getTopic().equals(topic)) {
				if (bestMsg == null) {
					bestMsg = m;
				}
				else {
					if (m.getAge() < bestMsg.getAge()) {
						bestMsg = m;
					}
				}
			}
			else {
				keepList.add(m);
			}
		}
		m_incomingMsgLst = keepList;
		m_lockIncoming.unlock();
		return bestMsg;
	}
	
	// Here, the latest message under the topic is returned.  It is not
	// deleted, so that this function can be called again with the expection
	// that if the message on the given topic has ever been received, it will
	// be avaliable.  If it has never been received, null is returned.
	public MqttMsg getMessage(String topic) {
		m_lockIncoming.lock();
		for (MqttMsg m: m_saveMsgLst) {
			if (m.getTopic().equals(topic)) {
				m_lockIncoming.unlock();
				return m;
			}
		}
		m_lockIncoming.unlock();
		return null;
	}

	// Clears out older messages to avoid too many.  All messages older than "age" in 
	// milliseconds will be deleted.
	public void clearOldMessages(long age) {
		ArrayList<MqttMsg> keepList = new ArrayList<MqttMsg>();
		
		m_lockIncoming.lock();
		for (MqttMsg m: m_incomingMsgLst) {
			if(m.getAge() < age) {
				keepList.add(m);
			}
		}
		m_incomingMsgLst = keepList;
		m_lockIncoming.unlock();
	}
	
	// Put a message in the queue to be sent to the broker.
	public void sendMessage(String topic, String text) {
		MqttMsg m = new MqttMsg(topic, text);
		m_lockOutgoing.lock();
		m_outgoingMsgLst.add(m);
		m_lockOutgoing.unlock();
	}
	
	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		//threadMessage("Mqtt: Delivery Complete.");
	}
	
	// Returns the number of messages sent since startup.
	public int getCountSent() {
		return m_nCountSent;
	}
	
	// Returns the number of messages received since startup.
	public int getCountReceived() {
		return m_nCountReceived;
	}
	
	// Returns the number of messages duplicated msgs..
	public int getCountDups() {
		return m_nCountDup;
	}
	
	// Returns the number of errors incountered since startup.
	public int getCountErrors() {
		return m_nCountErrors;
	}
	
	// Returns the number of errors incountered since startup.
	public int getCountSavedMsgs() {
		int n = 0;
		m_lockIncoming.lock();
		n = m_saveMsgLst.size();
		m_lockIncoming.unlock();
		return n;
	}
	
	// Function to log to the laptop.  Input can be a simple string, or
	// it can be a string formatted by String.format().
	public void logf(String fmt, Object... args) {
		String msg = String.format(fmt, args);
		sendMessage("robot/roborio/log", msg);
	}
}



	
