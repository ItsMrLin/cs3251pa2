import argparse
from RTP import *

rtpClient = RTP()
fileTerminator = "\0"
parser = argparse.ArgumentParser()
parser.add_argument("X", type=int)
parser.add_argument("A", help="the IP address of NetEmu")
parser.add_argument("P", help="the UDP port number of NetEmu", type=int)
args = parser.parse_args()

# # TAKE THESE OUT LATER \/
# print args.X
# print args.A
# print args.P
# # TAKE THOSE OUT LATER /\

done = False
while not done:
	print "Please enter a command ('exit' to quit):"
	command = raw_input()
	print '----------------------------------------\n'
	command = command.strip().lower()
	
	if command == 'connect':
		rtpClient.connectTo(args.X, args.A, args.P, 1500)

	if command == 'disconnect':
		rtpClient.close()

	if command.split(' ')[0] == 'get':
		filename = command.split(' ')[1]
		rtpClient.sendPacket('get '+filename+fileTerminator)
		doneski = False
		currentMessage = ""

		while not doneski:
		    data = rtpClient.readData('\0')
		    currentMessage += data
		    if fileTerminator in data:
		    	currentMessage = currentMessage[0:currentMessage.index(fileTerminator)]+currentMessage[currentMessage.index(fileTerminator)+1:]
        		currentMessage = currentMessage.strip()
		    	f = open(filename,'w')
		    	f.write(currentMessage)
		    	f.close()
		    	doneski = True



	if command.split(' ')[0] == 'post':
		filename = command.split(' ')[1]
		f = open(filename, 'r')
		rtpClient.sendPacket('POSTXKJSDLKJEBSJ1232423q2312p8hLASLDJKFASLJDBF21873EVOUFBLALNKHBV\n'+filename+'\n'+f.read()+fileTerminator)

	if command.split(' ')[0] == 'window':
		w = command.split(' ')[1]
		# do stuff
	if command == 'exit':
		rtpClient.sendPacket('close_server'+fileTerminator)
		done = True






