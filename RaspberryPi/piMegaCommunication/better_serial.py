import serial

class MegaCommunicator():
	distance = 0
	steps = 0
	leftSensor = 0
	rightSensor = 0
	checkSum = 0;
	theorySum = 0;

	port = serial.Serial("/dev/ttyAMA0",baudrate=9600,timeout=3.0)

	def readlineCR(self):
		rv=""
		while True:
			ch=self.port.read()
			rv+=ch
			if ch=='\r' or ch=='':
				return rv

	#wait for mega to start up
	def startup(self):
		print "Saying Hello"
		self.port.write("H")	
		print "Sent H"
		print "Arduino is reading"

		while True:
			ch = self.readlineCR()
			if(ch=='A'):
				print "Read:"
				print ch
				print "Sending ACK"
				self.port.write("A")
				print "Mega is ready"
				break

	def pollData(self):
		while True:
			print "Polling"
			self.port.write("P")
			#print "UltraSonic1:"
			self.distance = int(self.readlineCR())
			#print distance
			#print "Steps:"
			self.steps = int(self.readlineCR())
			#print ch 
			#print "Left Sensor:"
			self.leftSensor = int(self.readlineCR())
			#print ch
			#print "Right Sensor:"
			self.rightSensor = int(self.readlineCR())
			#print ch
			self.checkSum = int(self.readlineCR())
			break

	def checkError(self):
		self.theorySum =int(self.distance) + int(self.steps) + int(self.leftSensor) + int(self.rightSensor)
		print "theorySum:"
		print self.theorySum
		print "checkSum:"
		print self.checkSum
		#self.theorySum = 999
		if (self.theorySum != self.checkSum):
			print "CheckSum Error: please poll again"
		else:
			print "Data successfully polled"
###TEST
test = MegaCommunicator()
test.startup()
test.pollData()
print test.distance
print test.steps
print test.leftSensor
print test.rightSensor
test.checkError()
