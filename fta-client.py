import argparse
parser = argparse.ArgumentParser()
parser.add_argument("X", type=int)
parser.add_argument("A", help="the IP address of NetEmu")
parser.add_argument("P", help="the UDP port number of NetEmu", type=int)
parser.add_argument('commands',nargs='*', help='list of commands.')
args = parser.parse_args()
print args.X
print args.A
print args.P
print args.commands
