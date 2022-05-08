from socket import *
from datetime import datetime, timedelta
from textwrap import wrap
import sys
import time

receiverAddress = sys.argv[1]

receiverPortNum  = int(sys.argv[2])

senderPortNum = int(sys.argv[3])

timeoutInterval = int(sys.argv[4])

filename = sys.argv[5]

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', senderPortNum))
f = open(filename)
data = f.read()
f.close()

# this will turn file content into array of string, each has maxium length of 500
dataChunks = wrap(data, 500)

# get the list of sequence numbers we need to transmit
seqToTransmit = range(len(dataChunks))

def makePacket(seqNum):
	# from the sequence number, construct the package
	dataChunk = dataChunks[seqNum]
	return '1'+ '\n' + seqNum.__str__() + '\n' + len(dataChunk).__str__() + '\n' + dataChunk

while True:
	# transmit all packages
	for seqNum in seqToTransmit:
		clientSocket.sendto(makePacket(seqNum).encode(), (receiverAddress, receiverPortNum))
	# hear ack
	start = time.time()
	while ((time.time() - start) < (timeoutInterval/1000)):
		# maxium waittime is timeoutTime - currentTime
		clientSocket.settimeout(start+timeoutInterval/1000-time.time())
		try:
			message, clientAddress = clientSocket.recvfrom(2048)
		except:
			# timeout occured
			break
		decodedMessage = message.decode().split('\n', 3)
		msgType = int(decodedMessage[0])
		msgSeqnum = int(decodedMessage[1])
		if not (msgType == 0):
			print('not acknowledge packet type, error')
			break
		try:
			# remove received package's seqNum from list of sequence numbers to trasmit
			seqToTransmit.remove(msgSeqnum)
		except:
			# unexpected error, but should be fine to proceed
			print('might received duplicated packet sequence ack', msgSeqnum)

		if len(seqToTransmit) == 0:
			print('0 seq left to transmit')
			clientSocket.sendto('2\n'+len(dataChunks).__str__()+'\n0\n'.encode(), (receiverAddress, receiverPortNum))
			clientSocket.close()
			exit()
			

