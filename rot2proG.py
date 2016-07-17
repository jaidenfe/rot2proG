import serial
import time

'''
File: 	rot2proG.py
Author: Jaiden Ferraccioli
Brief: 	This class is a control interface for the SPID Elektronik rot2proG antenna rotor controller.
	This software was designed as an open source interface between the rotor controller and
	other systems. This can paired with an orbit propegator in order to extend usability and
	range of communication between an earth station and satellites or a communication station
	and a moving target. 
'''

class Rot2proG:

	pulse = 0
	debug = False

	def __init__(self, debugging=False):
		self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
		self.status()
		self.debug = debugging
		if(self.debug):
			print(self.ser.name)
			print("Pulse: " + str(self.pulse) + "\n")

	def __del__(self):
		self.ser.close()

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

		assert(ph == pv)
		self.pulse = ph

		if(self.debug):
			print("STATUS COMMAND SENT")
			print("Azimuth:   " + str(az))
			print("Elevation: " + str(el))
			print("PH: " + str(ph))
			print("PV: " + str(pv) + "\n")

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

		assert(ph == pv)
                self.pulse = ph

		if(self.debug):
			print("STOP COMMAND SENT")
			print("Azimuth:   " + str(az))
			print("Elevation: " + str(el))
                        print("PH: " + str(ph))
                        print("PV: " + str(pv) + "\n")

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
