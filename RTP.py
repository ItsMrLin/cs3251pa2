import socket
from pprint import pprint
from RtpPacket import *

class RTP:

    def __init__(self):
        pass

    """
        called by the server to set up the welcome socket
    """
    def setupRTPServer(self):
        self.welcomeSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        listen_addr = ("", 3001)
        self.welcomeSocket.bind(listen_addr)
        while True:
            # handle incoming syn packets
            data,addr = self.welcomeSocket.recvfrom(24)
            synPacketDictFromClient = stringToRtpPacketDict(data)
            print synPacketDictFromClient["sourcePort"]
            print "from address: " + str(addr)

    """
        called by client in order to establish a new connection with a server
    """
    def connectTo(self, serverIp, initialPacketSizeInByte = 1500):
        # only used for setting up connection
        initialSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        listen_addr = ("", 3000)
        initialSocket.bind(listen_addr)

        # set up initial packet
        synPacketDict = {}
        synPacketDict["sourcePort"] = 3000
        synPacketDict["destPort"] = 3001
        synPacketDict["syn"] = 1
        # convert 1500 into binary stored as a 32-bit (4 byte) string
        synPacketDict["data"] = fromBitsToString(str(bin(initialPacketSizeInByte))[2:], 4)
        synPacketString = rtpPacketDictToString(synPacketDict)
        # !IMPORTANT, otherwise checksum is going to be set as 0 automatically
        synPacketString = updatePacketStringChecksum(synPacketString)

        pprint("sending: "+synPacketString)
        initialSocket.sendto(synPacketString, (serverIp, 3001))

