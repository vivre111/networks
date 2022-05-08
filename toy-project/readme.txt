to run the program:
1. on [receiverServerAddress] [receiverPortNum],
   python a3receiver.py [receiverPortNum] [dropProbability] [writeFileName]
	 example: python a3receiver.py 9977 0 b.txt
2. on [senderServerAddress] [senderPortNum],
   python a3sender.py [receiverServerAddress] [receiverPortNum] [senderPortNum] [timeoutInMilliSeconds] [readFileName]
	 example: python a3sender.py ubuntu2004-002.student.cs.uwaterloo.ca 9977 9976 1000 a.txt


the program could be run on 
[receiverServerAddress]: ubuntu2004-002.student.cs.uwaterloo.ca
[senderServerAddress]: ubuntu2004-004.student.cs.uwaterloo.ca
[receiverPortNum]: 9977
[senderPortNum]: 9976

other parameters:
a3receiver.py will listen to incoming packets, drop them with probablity [dropProbablity], write the received file at [writeFileName]. It will send acknowledgement to sender, and generate logs.

a3sender.py will read [readFileName], send the data as packets to [receiverServerAddress] at [receiverPortNum], when waiting for acknowledgement, it has timeout [timeoutInMilliSeconds], it will run on portNumber [senderPortNum]





