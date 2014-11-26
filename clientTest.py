from RTP import *

rtpClient = RTP()
rtpClient.connectTo("127.0.0.1", 1500)
rtpClient.sendPacket("blah " * 1000)

rtpClient.close()

while True:
    continue