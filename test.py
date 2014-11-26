from RtpPacket import *
from RTP import *

# ------------------test 1----------------------
# dataString = "00000000000011110000000000000000"
# dataString = dataString + "00000000000000000000000000000000"
# dataString = dataString + "00000000000000000000000000000000"
# dataString = dataString + "00000000000000000000000000000000"
# dataString = dataString + "00000000000000000000000000000000"

# packetDic = stringToRtpPacketDict(fromBitsToString(dataString)+"hello!")
# rtpString = rtpPacketDictToString(packetDic)

# print "["+str(var["data"]) +"]"
# print rtpString


# -------------------test 2---------------------
# rtpPacketDict = {}
# # rtpPacketDict["sourcePort"] = 1234
# # rtpPacketDict["destPort"] = 5678
# # rtpPacketDict["seqNum"] = 123
# # rtpPacketDict["ackNum"] = 234
# # rtpPacketDict["extraHeaderLen"] = 0
# # rtpPacketDict["ack"] = 0
# # rtpPacketDict["rst"] = 0
# rtpPacketDict["syn"] = 1
# # rtpPacketDict["fin"] = 0
# # rtpPacketDict["receiveWindowSize"] = 10
# # rtpPacketDict["checksum"] = 0
# # rtpPacketDict["data"] = "It's a great day!"

# rtpString = rtpPacketDictToString(rtpPacketDict)
# # newRtpPacketDict = stringToRtpPacketDict(rtpString)

# rtpString = updatePacketStringChecksum(rtpString)
# pprint(rtpString)

# --------------------test 3----------------------
# ----------------establish connection: step 1------------
rtpServer = RTP()
rtpServer.setupRTPServer()

# in another script, run following
# from RTP import *
# rtpClient = RTP()
# rtpClient.connectTo("127.0.0.1")