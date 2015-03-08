'''
(c) Jan Papik 2015, email: it.jan.papik@gmail.com

Released under following licence:

	1) You may use, copy, modify, distribute this software all for non-commercial use.
	2) Preserve this licence.
	3) Also please refer to me as Author of this library.
	4) If you would like to use it commercial, please contact me.

Simple as that. Any future questions, bug report please direct to my email.

Usage & howto is at the end of file.
'''

import serial
import time

class SC800IM700:
	def __init__(self, device):
		self.ser = serial.Serial(device, baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=0.01)
		print("UART BRIDGE Connected")
	
	def readGPIO(self): #0 - 255 whole gpio must be set to input or qausidirectional
		self.ser.flushInput()
		self.ser.write('IP')
		value = self.ser.read()
		if value == '':
			raise Exception('readGPIO: No value Exception')
		print("Debug: readGPIO bin: " + str(bin(ord(value))))
		return ord(value);		
	
	def readRegister(self, address):
		self.ser.flushInput()
		
		charAdress = "".join(map(chr, [address]))
		self.ser.write('R' + charAdress + 'P')
		
		value = self.ser.read()
		if value == '':
			raise Exception('readRegister: No value Exception')
		print("Debug: readRegister bin: " + str(bin(ord(value))))
		return ord(value);	
		
	def writeRegister(self, address, data):
		self.ser.flushInput()
		
		charAdress = "".join(map(chr, [address, data]))
		self.ser.write('W' + charAdress + 'P')
		
		if self.readRegister(address) == data:
			print('Write to register was successful')
		else:
			raise Exception('Register data mismatch from written value.')
	
	def writeGPIO(self, data): #whole GPIO must be set to output or qausidirectional
		self.ser.flushInput()
		self.ser.write('O' + "".join(map(chr, [data])) + 'P')
	
	def setAllGPIO(self, type):
		if type == 'input':
			self.writeRegister(0x02, 0x55)
		elif type == 'output':
			self.writeRegister(0x02, 0xAA) #push-pull
			#bridge.writeRegister(0x02, 0xFF) #open-drain
		else:
			raise Exception('Unknown type, must be input or output')
	
	
		
	def write_byte_data(self, address, reg, value):
		#print("writing data\nAdress: " + str(address) + "\nReg: " + str(reg) + "\nData: " + str(value))
		#connection.write(bytes(['S', address << 1 + 1, reg, value,'P']))
		packet = packet = 'S' + "".join(map(chr, [((address << 1) & 0xfe ), 2, reg, value ])) + 'P'
#		print(packet)
#		print(["{:02x}".format(ord(i)) for i in packet])
		w = self.ser.write(packet)
#		print("Writed bytes: " + str(w))
#		print("Success")
	
	def write_byte(self, address, value):
		#print("writing byte\nAdress: " + str(address) + "\nData: " + str(value))

		packet = packet = 'S' + "".join(map(chr, [((address << 1) & 0xfe ), 1, value ])) + 'P'
#		print(packet)
#		print(["{:02x}".format(ord(i)) for i in packet])
		w = self.ser.write(packet)
#		print("Writed bytes: " + str(w))
#		print("Success")			
		
	def read_byte(self, address):
		print("read byte\nAdress: " + str(address) + "\n")

		packet = packet = 'S' + "".join(map(chr, [((address << 1) | 0x01 ), 1])) + 'P'
#		print(packet)
#		print(["{:02x}".format(ord(i)) for i in packet])
		
		self.ser.flushInput()
		w = self.ser.write(packet)
#		print("Writed control bytes: " + str(w))
		
		value = ''
		while value == '': #we must wait for incoming, it should take long time 
			value = self.ser.read()
		
		print("Read sucessful!!!!!!")
		
		return ord(value)
		
	def read_byte_data(self, address, reg):
		
#		print("reading data\nAdress: " + str(address) + "\nReg: " + str(reg))
		
		self.write_byte(address, reg)
		return self.read_byte(address)

class SMBus(SC800IM700):
	def __init__(self, port):
		SC800IM700.__init__(self, "/dev/ttyUSB0")	
		self.setAllGPIO('output')
	
'''
#Simple usage

In every python file using i2c type on the first line following:
import UARTtoI2C as smbus
Now you must copy this file to same folder as the file that is using it.
If it not work, check if device "/dev/ttyUSB0" exists, on Windows use:

class SMBus(SC800IM700):
	def __init__(self, port):
		SC800IM700.__init__(self, 0)	
		self.setAllGPIO('output')


#Advanced:
bridge = SC800IM700("/dev/ttyUSB0")
bridge.setAllGPIO('output')
bridge.writeGPIO(255)


#read GPIO on SC800IM700, read Register with adress 0x02 from SC800IM700, every 2 seconds
bridge.setAllGPIO('input')

while 1:
	c = bridge.readGPIO()
	print(c)
	c = bridge.readRegister(0x02)
	print(c)
	time.sleep(2)
'''


