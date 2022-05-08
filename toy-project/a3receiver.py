from socket import *
import sys
from random import random

receiverPortNum = int(sys.argv[1])
dropProb = float(sys.argv[2])
wfilename = sys.argv[3]

def makeAckPacket(seqNum):
	# given sequence number, generate content of ack
	return '0'+ '\n' + seqNum.__str__() + '\n' + '0' + '\n' 

serverSocketUDP = socket(AF_INET, SOCK_DGRAM)
serverSocketUDP.bind(('', receiverPortNum))

# to record received data as a array of string, with ith index equals string with sequence number i
recvList = []
# to generate log which record received sequence numbers
recvLog = []
# to generate log which record dropped sequence numbers
dropLog = []

while True:
	# listen to UDP client at the port number
	message, clientAddress = serverSocketUDP.recvfrom(2048)
	decodeMessage = message.decode().split('\n', 3)
	msgType = decodeMessage[0]
	msgSeqnum = int(decodeMessage[1])
	msgLen = int(decodeMessage[2])
	msgData = decodeMessage[3]
	if(msgType == '2'):
		recvLog.append(msgSeqnum.__str__())
		print('received all content, end task')
		break
	if(random()<dropProb):
		# drop the package
		dropLog.append(msgSeqnum.__str__())
		continue
	# add to arrival log
	recvLog.append(msgSeqnum.__str__())
	# remember the data
	if len(recvList) <= msgSeqnum:
		recvList.extend(['']*(msgSeqnum-len(recvList)+1))
	if not (recvList[msgSeqnum]==''):
		print('received duplicate, discard package', msgSeqnum)
		continue
	recvList[msgSeqnum] = msgData
	# send acknowledgement
	serverSocketUDP.sendto(makeAckPacket(msgSeqnum).encode(), clientAddress)
		
serverSocketUDP.close()


def listToString(s, cont = ''):
	# turn a list of string to a string
	# initialize an empty string
	str1 = ""
	# traverse in the string
	for ele in s:
			str1 += ele
			str1 += cont
	# return string
	return str1

f = open(wfilename, "w")
f.write(listToString(recvList))
f.close()
f = open('arrival.log', "w")
f.write(listToString(recvLog, '\n'))
f.close()
f = open('drop.log', "w")
f.write(listToString(dropLog, '\n'))
f.close()



