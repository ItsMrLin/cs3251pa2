# author: Zhiyuan Lin

import socket
from pprint import pprint
from RtpPacket import *

class RTP:

    def __init__(self):
        pass

    """
        called by the server to set up the welcome socket
        handler is provided by the application that uses rtp in order to handle incoming test
        handler should be a call back function with parameters like function(data, client_address, rtpInstance for sending data back)
    """
    def setupRTPServer(self, handler):
        # setting up initial welcome RTP instance variables
        # due to NetEmu port number limitation we no longer support this
        # self.nextServerPortNum = 5001
        # self.connectionList = []

        self.dataSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        listen_addr = ("", 3001)
        self.dataSocket.bind(listen_addr)
        while True:
            # handle incoming syn packets
            data, addr = self.dataSocket.recvfrom(24)
            synPacketDictFromClient = stringToRtpPacketDict(data)

            # create new RTP instance for actual data transfer
            packetSize = ord(synPacketDictFromClient["data"][3]) + ord(synPacketDictFromClient["data"][2])*256 + ord(synPacketDictFromClient["data"][1])*65536 + ord(synPacketDictFromClient["data"][0])*16777216
            self._initializeDataSocket(3001, addr, packetSize)

            # print int(fromBitsToString([2:], 4), 2)
            print "from address: " + str(addr[1])
            # rtpInstance = new rtp instance with new port
            # handler(synPacketDictFromClient["data"], addr, rtpInstance)

    """
        called by the welcome server whenever there's a request for new RTP connection
        to initialize the rtp instance used for sending actual data
    """
    def _initializeDataSocket(self, portNum, destAddr, packetSize = 1500):
        self.port = portNum
        self.packetSize = packetSize
        self.destAddr = destAddr


    """
        called by client in order to establish a new connection with a server
    """
    def connectTo(self, serverIp, initialPacketSizeInByte = 1500):
        # only used for setting up connection
        self.dataSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        listen_addr = ("", 3000)
        self.dataSocket.bind(listen_addr)
        self._initializeDataSocket(3000, (serverIp, 3001), initialPacketSizeInByte)

        # set up initial packet
        synPacketDict = {}
        synPacketDict["syn"] = 1
        # convert 1500 into binary stored as a 32-bit (4 byte) string
        self._sendPacket(fromBitsToString(str(bin(initialPacketSizeInByte))[2:], 4), synPacketDict)


        

    """
        called by RTP instance for sending data
    """
    def _sendPacket(self, data, extraDict = {}):
        packetDict = {}
        packetDict["sourcePort"] = self.port
        packetDict["destPort"] = self.destAddr[1]
        packetDict["data"] = data

        for key in extraDict:
            packetDict[key] = extraDict[key]

        # checksum
        synPacketString = rtpPacketDictToString(packetDict)
        # !IMPORTANT, otherwise checksum is going to be set as 0 automatically
        synPacketString = updatePacketStringChecksum(synPacketString)

        # sending over UDP
        pprint("sending: " + synPacketString)
        self.dataSocket.sendto(synPacketString, self.destAddr)





