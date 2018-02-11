// --------------------------------------------------------------------
// StopWatch.java -- Class to get high precision timing info.
//
// Created 3/19/17 DLB
// --------------------------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

import java.util.Date;

// Class to deal with timestamps and measuring time.
public class StopWatch {
	// Returns a timestamp useful for marking events to millisecond precision.
	public static long timestamp() {
		Date d = new Date();
		return d.getTime();
	}
	
	// Returns a start value for a stopwatch.  The token
	// returned should be given to stop() to measure
	// elapse time.
	public static long start() {
		Date d = new Date();
		return d.getTime();
	}
	
	// Returns the time elapse (in milliseconds) since
	// the call to start(), given the return value from
	// start.
	public static long stop(long timestamp) {
		Date d = new Date();
		return d.getTime() - timestamp;
	}
}
