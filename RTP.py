import socket
import Queue
from pprint import pprint
from RtpPacket import *
import threading
import time
import sys
from random import randint

class RTP:

    def __init__(self):
        pass

    def _sendSimpleAck(self,ackNum):
        rtpPacketDict = {}
        rtpPacketDict["sourcePort"] = self.port
        rtpPacketDict["destPort"] = self.destAddr[1]
        rtpPacketDict["ack"] = 1
        rtpPacketDict["ackNum"] = ackNum
        rtpPacketDict["data"] = ' '*(self.packetSize-20)
        rtpstring = rtpPacketDictToString(rtpPacketDict)
        rtpstring = updatePacketStringChecksum(rtpstring)
        self.sending_queue.put(rtpstring)
        
    def _acknowledge(self, packetDict):
        #do stuff. ack the things
        if self.sending_queue.qsize() > 0:
            done = False
            for i in range(0,self.sending_queue.qsize()):
                rtpstring = self.sending_queue.get()
                rtpDict = stringToRtpPacketDict(rtpstring)
                if rtpDict["ack"] == 0 and not done:
                    rtpDict["ack"] = 1
                    rtpDict["ackNum"] = packetDict["seqNum"] + 1
                    self.sending_queue.put(rtpPacketDictToString(rtpDict))
                    done = True
                else:
                    self.sending_queue.put(rtpstring)
            if not done:
                self._sendSimpleAck(packetDict["seqNum"] + 1)
        else:
            self._sendSimpleAck(packetDict["seqNum"] + 1)


    def listener(self):
        while True:
            time.sleep(0.1)

            try:
                rtpstring = self.dataSocket.recvfrom(self.packetSize)[0]
            except socket.timeout:
                sys.exit(0)

            if not (rtpstring == None or len(rtpstring) < self.packetSize):
                # print 'CHECKSUM NOT CLEARED YET: '+ str(stringToRtpPacketDict(rtpstring))
                # print "check listener!"
                rtpDict = stringToRtpPacketDict(rtpstring)

                pprint("RECEIVED: seqNum=" + str(rtpDict["seqNum"]) + " ackNum=" + str(rtpDict["ackNum"]) + " ack=" + str(rtpDict["ack"])  + " fin=" + str(rtpDict["fin"]))
                pprint("RECEIVED1: seqNum="+ str(rtpDict["seqNum"]) + "packet CheckSum="+ str(rtpDict["checksum"]) + "Sender checksum=" + str(bsdChecksum(rtpstring)) + "packet len="+ str(len(rtpstring)) )

                if bsdChecksum(rtpstring) == rtpDict["checksum"]:
                    # if it is an ack package, we pop things out from not_acked_queue
                    if rtpDict["ack"] == 1:
                        for i in range(0,len(self.not_acked_queue)):
                            not_acked_dict = stringToRtpPacketDict(self.not_acked_queue[i])
                            # pprint("ACK: not acked seqNum=" + str(not_acked_dict["seqNum"]) + "ackNum-1=" + str(rtpDict["ackNum"] - 1))
                            if not_acked_dict["seqNum"] == rtpDict["ackNum"] - 1: # if you received an ack for it.
                                self.not_acked_queue.pop(i)
                                break
                    
                    # print 'CHECKSUM CLEARED: '+ str(stringToRtpPacketDict(rtpstring))

                    # if the payload is not empty, ack it and put it in buffer
                    # second condition below is so we don't acknowledge straight up acks
                    if (not len(rtpDict["data"].strip())==0):
                        self.received_buffer.put((rtpDict["seqNum"],rtpDict["data"]))
                        self._acknowledge(rtpDict)
                    else:
                        # if payload is empty, check if it's a fin
                        if (rtpDict["fin"] == 1):
                            self.readyToClose = True
                            self._acknowledge(rtpDict)
                            self.close()

                else:
                    print 'CHECKSUM DID NOT CLEAR!'
            else:
                if not len(rtpstring) == self.packetSize:
                    print "Something went wrong. Packet recv'ed is a different length from packetSize."


    def sender(self):
        while True:
            time.sleep(0.5)
            if not self.sending_queue.empty():
                # print "check sender!"
                rtpstring = self.sending_queue.get()
                rtpDict = stringToRtpPacketDict(rtpstring)
                # -------------FOR DEBUGGING-------------
                pprint("sent: seq=" + str(rtpDict["seqNum"]) + " ackNum=" + str(rtpDict["ackNum"]) + " ack=" + str(rtpDict["ack"]) + " fin=" + str(rtpDict["fin"]))
                # -------------END FOR DEBUGGING-------------
                self.dataSocket.sendto(rtpstring, self.destAddr)
                # if seqNum is 0, it's a simple ack packet or fin, which does not require ack
                if (rtpDict["seqNum"] != 0):
                    self.not_acked_queue.append(rtpstring)

            #TODO: resend not_acked things after a certain amount of time

    """
        called by the server to set up the welcome socket
        handler is provided by the application that uses rtp in order to handle incoming test
        handler should be a call back function with parameters like function(data, rtpInstance for sending data back)
    """
    def _setupRTPServer(self):
        # setting up initial welcome RTP instance variables
        # due to NetEmu port number limitation we no longer support this
        # self.nextServerPortNum = 5001
        # self.connectionList = []

        self.dataSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        listen_addr = ("", 3001)
        self.dataSocket.bind(listen_addr)

        #JUST FOR TESTING MOVE LATER -----\/
        # self._initializeDataSocket(3001, 'panda')

        # thread.start_new_thread(self.sender,())

        # thread.start_new_thread(self.listener,())
        #---------------------------------/\

        while True:
            # handle incoming syn packets
            # in order to get addr, cannot use self._receivePacket here
            data, addr = self.dataSocket.recvfrom(24)
            synPacketDictFromClient = stringToRtpPacketDict(data)
            # print "get initail syn!"
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
                    tSender = threading.Thread(target=self.sender)
                    tSender.daemon = True
                    tSender.start()
                    tListener = threading.Thread(target=self.listener)
                    tListener.daemon = True
                    tListener.start()
                    tSender.join()
                    tListener.join()


    def setupRTPServer(self):
        tSender = threading.Thread(target=self._setupRTPServer)
        tSender.daemon = True
        tSender.start()

    """
        called by the welcome server whenever there's a request for new RTP connection
        to initialize the rtp instance used for sending actual data
    """
    def _initializeDataSocket(self, portNum, destAddr, packetSize = 1500):
        self.port = portNum
        self.packetSize = packetSize
        self.destAddr = destAddr
        self.readyToClose = False
        self.dataSocket.settimeout(60) #60 seconds
        self.seqNum = randint(0,4000000)

        # initialize queues here
        self.sending_queue = Queue.Queue()
        self.not_acked_queue = []
        self.received_buffer = Queue.PriorityQueue()




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
        self._sendPacket(fromBitsToString(str(bin(initialPacketSizeInByte))[2:], 4), {"syn": 1})
        # waiting for server side ack
        ackFromServerForSyn = self._receivePacket()
        # print "received ack from server"
        ackFromServerForSynDict = stringToRtpPacketDict(ackFromServerForSyn)
        if (ackFromServerForSynDict['checksum'] == bsdChecksum(ackFromServerForSyn) and ackFromServerForSynDict['ack'] == 1):
            # send ack back to server
            self._sendPacket("", {"ack": 1})

            # ---------FINISH HANDSHAKE ON THE CLIENT SIDE----------
            try:
                # thread.start_new_thread(self.sender,())
                # thread.start_new_thread(self.listener,())
                tSender = threading.Thread(target=self.sender)
                tSender.daemon = True
                tSender.start()
                tListener = threading.Thread(target=self.listener)
                tListener.daemon = True
                tListener.start()
            except:
                print "THREAD DID NOT RUN!"
                

        

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
        called by the client to send data

        splits sending payload into packets and adds them to the sending queue
    """
    def sendPacket(self, data):
        # dataBits = fromStringToBits(data)
        numPackets = 1
        if len(data)+20 > self.packetSize:
            numPackets = int(len(data)/(self.packetSize-20)) + 1

        for i in range(0, numPackets):
            rtpPacketDict = {}
            rtpPacketDict["sourcePort"] = self.port
            rtpPacketDict["destPort"] = self.destAddr[1]
            rtpPacketDict["seqNum"] = self.seqNum
            self.seqNum += self.packetSize
            rtpPacketDict["extraHeaderLen"] = 0
            if i <numPackets-1:
                rtpPacketDict["data"] = data[i*(self.packetSize-20): (i+1)*(self.packetSize-20)]
            else:
                rtpPacketDict["data"] = data[i*self.packetSize:]
                rtpPacketDict["data"] = rtpPacketDict["data"] + (' '*(self.packetSize - len(rtpPacketDict["data"]) - 20))

            rtpstring = rtpPacketDictToString(rtpPacketDict)
            rtpstring = updatePacketStringChecksum(rtpstring)
            pprint("SENDING: seqNum="+ str(rtpPacketDict["seqNum"]) + "Sender checksum=" + str(bsdChecksum(rtpstring)) + "packet len=" + str(len(rtpstring)))
            # print len(rtpstring)
            self.sending_queue.put(rtpstring)
            # print "clientsize send queue size: ", self.sending_queue.qsize()

    """
        called by the server to shutdown the server
    """
    def shutdown():
        pass

    """
        called by the client in order to close the connection
    """
    def close(self):
        # if the other side did not close before, send a fin to notify 
        if (not self.readyToClose):
            finDict = {
                "sourcePort": self.port,
                "destPort": self.destAddr[1],
                "seqNum": 0,
                "fin": 1,
                "data": ' '*(self.packetSize-20)
            }
            self.seqNum += 20

            # checksum
            finDictString = rtpPacketDictToString(finDict)
            # !IMPORTANT, otherwise checksum is going to be set as 0 automatically
            finDictString = updatePacketStringChecksum(finDictString)

            self.sending_queue.put(finDictString)

            # if get a fin before, i.e. the other side is finished
            while not (self.sending_queue.empty() and (not self.not_acked_queue)):
                pprint("CLOSE: sending_queue size=" + str(self.sending_queue.qsize()) + " not_acked_queue size=" + str(len(self.not_acked_queue)))
                time.sleep(1)
        # when all data sent and acknowledged
        pprint("CLOSED") 
        sys.exit(0)    
