import argparse
from RtpPacket import *
from RTP import *
import sys

rtpServer = RTP()
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

rtpServer.setupRTPServer(args.X)

currentMessage = ""

while True:
    try:
        print 'Set up'
        data = rtpServer.readData('\0')
        currentMessage += data
        if '\0' in data:
            currentMessage = currentMessage[0:currentMessage.index('\0')]+currentMessage[currentMessage.index('\0')+1:]
            currentMessage = currentMessage.strip()
            if len(currentMessage.split(' ')) == 2 and currentMessage.split(' ')[0] == 'get':
                filename = currentMessage.split(' ')[1]
                f = open(filename,'r')
                rtpServer.sendPacket(f.read+'\0')

            if currentMessage.split('\n')[0] == 'POSTXKJSDLKJEBSJ1232423q2312p8hLASLDJKFASLJDBF21873EVOUFBLALNKHBV':
                filename = currentMessage.split['\n'][1]
                filedata = currentMessage.split('\n')[2:]
                f = open(filename,'w')
                for dat in filedata:
                    f.write(dat)
                f.close()
            if currentMessage == 'close_server':
                sys.exit(0)
    except:
        print 'Not connected'





    


