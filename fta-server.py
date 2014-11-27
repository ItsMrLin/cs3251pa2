import argparse
from RtpPacket import *
from RTP import *

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

while True:
    


