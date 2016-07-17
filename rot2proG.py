'''
File: 	rot2proG.py
Author: Jaiden Ferraccioli
Brief: 	This class is a control interface for the SPID Elektronik rot2proG antenna rotor controller.
	This software was designed as an open source interface between the rotor controller and
	other systems. This can paired with an orbit propegator in order to extend usability and
	range of communication between an earth station and satellites or a communication station
	and a moving target. 
'''

import serial
import time

'''
This class defines the control interface for the SPID Elektronik rot2proG antenna rotor controller.

Note: 	The controller will not change azimuth or elevation values unless the rotor is connected.

Setup:	The controller must be set to use the "SPID" protocol. To do this, press the 'S' button on the
	controller until it says 'PS' along with the current azimuth and elevation. Then the left or
	right buttons on the controller to change between protocols. Select the protocol saying 'SP' in
	the 'Horizontal' field of the controller. Once the controller is set to use the SPID protocol,
	we must put it into automated mode. To do this, press the 'F' button until the controller reads
	'A' along with the current azimuth and elevation. You are now ready to communicate with the
	rotor controller.
'''
class Rot2proG:

	pulse = 0
	debug = False

	'''
	This sets up the serial connection and pulse value.
	When set to true, the debugging parameter allows for information such as
	asimuth, elevation and pulse to be printed out when functions are called.
	Debugging defualts to False.
	'''
	def __init__(self, debugging=False):
		self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
		self.status()
		self.debug = debugging
		if(self.debug):
			print(self.ser.name)
			print("Pulse: " + str(self.pulse) + "\n")

	'''
	This makes sure that the serial connection is closed when the class is deleted 
	or the program terminates
	'''
	def __del__(self):
		self.ser.close()

	'''
	Send a STATUS command to the controller, which requests the current azimuth
	and elevation of the rotor. The azimuth, elevation and pulse are then computed,
	the pulse is set and the azimuth, elevation and pulse are returned as a list (first
	element being azimuth, the second being elevation, and the third being pulse).
	'''
	def status(self):
		cmd = ['\x57','\x00','\x00','\x00','\x00','\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x1f', '\x20']
		packet = "".join(cmd)
		
		self.ser.write(packet)
		self.ser.flush()

		rec_packet = self.ser.read(12)

		az = (ord(rec_packet[1]) * 100) + (ord(rec_packet[2]) * 10) + ord(rec_packet[3]) + (ord(rec_packet[4]) / 10) - 360.0
		el = (ord(rec_packet[6]) * 100) + (ord(rec_packet[7]) * 10) + ord(rec_packet[8]) + (ord(rec_packet[9]) / 10) - 360.0
		ph = ord(rec_packet[5])
		pv = ord(rec_packet[10])

		ret = [az, el, ph]

		assert(ph == pv)
		self.pulse = ph

		if(self.debug):
			print("STATUS COMMAND SENT")
			print("Azimuth:   " + str(az))
			print("Elevation: " + str(el))
			print("PH: " + str(ph))
			print("PV: " + str(pv) + "\n")

		return ret

	'''
	Send a STOP command to the controller, which causes the rotor to stop moving and
	return the current azimuth, elevation and pulse of the rotor where it stopped. The
	azimuth, elevation and pulse are then computed, the pulse is set and the azimuth,
	elevation and pulse are returned as a list (first element being azimuth, sencond
	being elevation and the third being pulse).
	'''
	def stop(self):
		cmd = ['\x57','\x00','\x00','\x00','\x00','\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x0f', '\x20']
		packet = "".join(cmd)

		self.ser.write(packet)
		self.ser.flush()

		rec_packet = self.ser.read(12)

		az = (ord(rec_packet[1]) * 100) + (ord(rec_packet[2]) * 10) + ord(rec_packet[3]) + (ord(rec_packet[4]) / 10) - 360.0
                el = (ord(rec_packet[6]) * 100) + (ord(rec_packet[7]) * 10) + ord(rec_packet[8]) + (ord(rec_packet[9]) / 10) - 360.0
		ph = ord(rec_packet[5])
                pv = ord(rec_packet[10])

		ret = [az, el, ph]

		assert(ph == pv)
                self.pulse = ph

		if(self.debug):
			print("STOP COMMAND SENT")
			print("Azimuth:   " + str(az))
			print("Elevation: " + str(el))
                        print("PH: " + str(ph))
                        print("PV: " + str(pv) + "\n")

		return ret

	'''
	send a SET command to the controller, which causes the rotor to adjust its position
	to the azimuth and elevation specified by the azi and eli parameters respecitvely.
	The azi and eli parameters are floating point values that specify the desired position.
	There is no response to the SET command, thus nothing to return.
	'''
	def set(self, azi, eli):
		az = "0" + str((self.pulse * (azi + 360)))
		el = "0" + str((self.pulse * (eli + 360)))

		cmd = ['\x57', az[-4], az[-3], az[-2], az[-1], chr(self.pulse), el[-4], el[-3], el[-2], el[-1], chr(self.pulse), '\x2f', '\x20']
		packet = "".join(cmd)

		self.ser.write(packet)
		self.ser.flush()

		if(self.debug):
			print("SET COMMAND SENT")
			print("Sent: " + packet)
			print("Set Azimuth:   " + str(azi) + " (" + str(az) + ")")
			print("Set Elevation: " + str(eli) + " (" + str(el) + ")")
			print("Pulse: " + chr(self.pulse) + "\n")

		time.sleep(1)

	'''
	Calls the STATUS, STOP and SET functions multiple times
	in order to test the rot2proG class functionality
	'''
	def test(self):
		rot = Rot2proG(True)
		rot.status()
		rot.stop()
		rot.set(209, 13)
		rot.status()
		time.sleep(3)
		rot.status()
		time.sleep(10)
		rot.set(19, 144)
		rot.status()
		rot.stop()
