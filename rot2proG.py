import serial

class Rot2proG:
	
	def __init__(self):
		self.ser = serial.Serial(port='/dev/ttyUSB2',baudrate=600, bytesize=8, parity='N', stopbits=1, timeout=None)
		print(self.ser.name)

	def __del__(self):
		self.ser.close()

	def status(self):
		hex_char = ['0x57','0x00','0x00','0x00','0x00','0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x1f', '0x20']
		packet = "".join(hex_char)
		
		self.ser.write(packet)

		self.ser.flush()

		print("Sent: " + packet)
		print("Received: " + self.ser.read(12))

if __name__ == "__main__":
	rot = Rot2proG()
	rot.status()
