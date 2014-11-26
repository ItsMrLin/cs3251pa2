from RTP import *

rtpClient = RTP()
rtpClient.connectTo("127.0.0.1", 100)
rtpClient.sendPacket("blah " * 100)

rtpClient.close()

while True:
    continue