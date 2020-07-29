import I2CtoUART

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
