import serial

class MegaCommunicator():
	gloveSensor = 0
	frontSensor = 0
	leftSensor = 0
	rightSensor = 0
	steps = 0
	orientation_tag = 0
	checkSum = 0
	theorySum = 0

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
		print "Arduino is reading.."

		while True:
			ch = self.readlineCR()
			#ch = self.port.read()
			print ch
			if(ch=='A'):
				print "Arduino reads:"
				print ch
				print "Sending ACK"
				self.port.write("A")
				print "Mega is ready"
				break

	def pollData(self):
		while True:
			print "Polling..."
			self.port.write("P")
			#print "gloveSensor:"
			self.gloveSensor = int(self.readlineCR())
			#print gloveSensor
			#print "frontSensor:"
			self.frontSensor = int(self.readlineCR())
			#print frontSensor 
			#print "Left Sensor:"
			self.leftSensor = int(self.readlineCR())
			#print leftSensor
			#print "Right Sensor:"
			self.rightSensor = int(self.readlineCR())
			#print rightSensor
			#print "steps:"
			self.steps = int(self.readlineCR())
			#print "orientation_tag:"
			self.orientation_tag = int(self.readlineCR())
			#print "checkSum:"
			self.checkSum = int(self.readlineCR())
			break

	def checkError(self):
		self.theorySum =int(self.gloveSensor) + int(self.frontSensor) + int(self.leftSensor) + int(self.rightSensor)+ int(self.orientation_tag) + int(self.steps)
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

print test.gloveSensor
print test.frontSensor
print test.leftSensor
print test.rightSensor
print test.steps
print test.orientation_tag
test.checkError()

test.pollData()
print test.gloveSensor
print test.frontSensor
print test.leftSensor
print test.rightSensor
print test.steps
print test.orientation_tag
