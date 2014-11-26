"""
Perry Transport Protocol welcomer class

this class runs on the welcome port 80 and spawns ptp 
objects everytime a connection is asked for.

Takes care of the 3 part handshake and spawns a ptp 
object for the connection on the 2nd ack.
"""
from ptp import ptp

class welcomer():
	def __init__(ip):
		self.connections = {}
		# set up connection on port 80 and start listening