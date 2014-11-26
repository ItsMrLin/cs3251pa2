# author: Zhiyuan Lin

import socket
import Queue
from pprint import pprint
from RtpPacket import *
import thread
import time

class RTP:

    def __init__(self):
        pass

    """
        called by the server to set up the welcome socket
        handler is provided by the application that uses rtp in order to handle incoming test
        handler should be a call back function with parameters like function(data, rtpInstance for sending data back)
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
            # in order to get addr, cannot use self._receivePacket here
            data, addr = self.dataSocket.recvfrom(24)
            synPacketDictFromClient = stringToRtpPacketDict(data)

            if (synPacketDictFromClient['checksum'] == bsdChecksum(data) and synPacketDictFromClient['syn'] == 1):
                # create new RTP instance for actual data transfer
                packetSize = ord(synPacketDictFromClient["data"][3]) + ord(synPacketDictFromClient["data"][2])*256 + ord(synPacketDictFromClient["data"][1])*65536 + ord(synPacketDictFromClient["data"][0])*16777216
                self._initializeDataSocket(3001, addr, packetSize)

                # send ack back to client
                self._sendPacket("", {"ack": 1})
                
                # # wait for ack from client
                ackFromClient = self._receivePacket()
                ackFromClientDict = stringToRtpPacketDict(ackFromClient)
                if (ackFromClientDict['checksum'] == bsdChecksum(ackFromClient) and ackFromClientDict['ack'] == 1):
                    print "BOOM! from address: " + str(addr[1])

                    # ------------FINISH HANDSHAKE--------------
                    # PAV: start spawning thread receiving packets using _receivePacket
                    # good reference for multithreading: http://stackoverflow.com/questions/2846653/python-multithreading-for-dummies
                    # handler(synPacketDictFromClient["data"], addr, rtpInstance)

    def listen(self,threadname,delay):
        while true:

        return

    """
        called by the welcome server whenever there's a request for new RTP connection
        to initialize the rtp instance used for sending actual data
    """
    def _initializeDataSocket(self, portNum, destAddr, packetSize = 1500):
        self.port = portNum
        self.packetSize = packetSize
        self.destAddr = destAddr
        self.dataSocket.settimeout(60) #60 seconds


        # initialize queues here
        self.sending_queue = Queue.Queue()
        self.not_acked_queue = Queue.Queue()
        self.received_queue = Queue.Queue()



    """
        called by client in order to establish a new connection with a server
    """
    def connectTo(self, serverIp, initialPacketSizeInByte = 1500):
        # only used for setting up connection
        self.dataSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        listen_addr = ("", 3000)
        self.dataSocket.bind(listen_addr)
        self._initializeDataSocket(3000, (serverIp, 3001), initialPacketSizeInByte)

        # convert 1500 into binary stored as a 32-bit (4 byte) string
        pprint(fromBitsToString(str(bin(initialPacketSizeInByte))[2:], 4))
        self._sendPacket(fromBitsToString(str(bin(initialPacketSizeInByte))[2:], 4), {"syn": 1})
        # waiting for server side ack
        ackFromServerForSyn = self._receivePacket()
        ackFromServerForSynDict = stringToRtpPacketDict(ackFromServerForSyn)
        if (ackFromServerForSynDict['checksum'] == bsdChecksum(ackFromServerForSyn) and ackFromServerForSynDict['ack'] == 1):
            # send ack back to server
            self._sendPacket("", {"ack": 1})

        

    """
        called by RTP instance for sending single data packet
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
        self.dataSocket.sendto(synPacketString, self.destAddr)

    """
        called by RTP instance for receiving single data packet
    """
    def _receivePacket(self, packetSize = None):
        if packetSize is None:
            packetSize = self.packetSize
        return self.dataSocket.recvfrom(packetSize)[0]

    """
        called by the server to shutdown the server
    """
    def shutdown():
        pass

    """
        called by the client in order to close the connection
    """
    def close():
        pass

