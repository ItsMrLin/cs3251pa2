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


	if command.split(' ')[0] == 'post':
		filename = command.split(' ')[1]
		f = open(filename, 'r')
		rtpClient.sendPacket(f.read()+fileTerminator)

	if command.split(' ')[0] == 'window':
		w = command.split(' ')[1]
		# do stuff
	if command == 'exit':
		rtpClient.sendPacket('close_server'+fileTerminator)
		done = True






