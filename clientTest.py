from RTP import *

rtpClient = RTP()
rtpClient.connectTo("127.0.0.1")
rtpClient.sendPacket("blah blah blah blah")