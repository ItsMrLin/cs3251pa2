import argparse
parser = argparse.ArgumentParser()
parser.add_argument("X", help="the port number at which the fta-server’s UDP socket should bind to (odd number)", type=int)
parser.add_argument("A", help="the IP address of NetEmu")
parser.add_argument("P", help="the UDP port number of NetEmu", type=int)
args = parser.parse_args()
print args.X
print args.A
print args.P
