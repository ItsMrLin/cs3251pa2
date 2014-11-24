"""
This is the Perry Transport Protocol

Our Reliable Transport Protocol (RTP) is an improved version of 
Transmission Control Protocol (TCP), but with better performance, 
more secure data transmitting, a more concise header, and improved 
connection management.

"""
class ptp:
	"""
	Each ptp object represents one ptp connection
	"""

	def __init__(self, _ip, _port, _timeout=50): #timeout in ms
		self.ip = _ip
		self.port = _port
		self.timeout = _timeout
		self.not_acked_queue = []
		self.sending_queue = []
		self.recv_buffer = []


	def _listen():
		"""
		This method creates a socket that is global to the ptp 
		instance and starts listening on that socket.
		whenever there's a packet coming in, we put it in the buffer

		Takes care of:
		socket()
		socket.bind()
		socket.listen()

		"""
		
		# def _receive():
		# 	"""
		# 	Receive individual packets
		# 	and put things in queue/buffer
		# 	Move it into the thread obj. created in _listen()
		# 	
		# 	"""
		# 	return True
	
		#code things		
		return True
		#can we set up some sort of callback framework for when a 
		#connection is established?

	def _send():
		"""
		This will also go into it's own thread that will check the
		not-acked queue and sending queue

		Send individual packets
		
		"""
		
		return True
		
	def establishConnection(destIp, destPort, packetsize=24): #in bytes
		"""
		Send the initial request for a connection establishment

		"""
		return True

	def send(data):
		"""
		break packets and add to the sending_queue()
		"""
		return True

	def recv():
		"""
		receive packet and add it to the buffer

		send an Ack back
		"""
		return True
	

	def destroy():
		"""
		Handles our special tear down.

		As a general rule we establish that if any end-point does not 
		receive a packet for 60 seconds, it closes the connection. The 
		official procedure for terminating connections is as follows. 
		When end-point A does not have any data to send A sends a FIN 
		(resending it if it does not get an ACK after a normal packet 
		timeout). B sends an ACK. A receives this ACK and releases 
		resources for it’s sending queue and not-acked queue. A is not 
		done sending data, but B may still be sending data to A.

		When B is done sending data to A, it sends a FIN and closes. If 
		A receives the FIN it closes immediately, otherwise it closes 
		after 60 seconds. 

		"""
		return True

