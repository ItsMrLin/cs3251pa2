from RTP import *

rtpClient = RTP()
# rtpClient.connectTo(args.X, args.A, args.P, 1500)
rtpClient.connectTo(3000, "127.0.0.1", 8000, 100)
rtpClient.sendPacket("blah \0" * 100)

# rtpClient.close()

while True:
    continue