#!/usr/bin/ python

import socket
import time
import helpers from Socket

"""
Group File (This will get created by trackers)

- Get data from seeders
	- Respond to leechers' request
	- If there is no leecher request for a finite time, suicide
"""


class Group():

	def __init__(self, ip=None, port=None, ttl=1,seeders=None):
		if not (ip or port or seeders) :
			print "Group required IP and port and seeders list"
			exit()

		#addrinfo = socket.getaddrinfo(ip, None)[0]
		# create a UDP socket with got family addrinfo[0]
		#s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
		s1 = Socket(ip,port).UDP()
		# Set Time-to-live (optional)
		ttl_str = struct.pack('@i', ttl)

		# include ttl into IP header
		s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_str)
# for udp
		# assign variable to group self
		self.socket1 = s1
		self.ip = ip
		self.port= port
		self.ttl = ttl
		self.socket.bind(ip, port)



## for tcp
		port2 = 8888
		s1 = Socket(ip,port2).TCP()
		self.socket2 = s2
		self.ip = ip
		self.port2 = port2
		#self.ttl = ttl
		self.socket.bind(ip, port2)

	"""
	Send data to an ip and port
	"""
	def send(self, data):
		self.socket.sendto(data + '\0', (self.ip, self.port))
		while True:
			print "waiting to  receiver"
			data, receiver = self.socket.recvfrom(1500)
			print ("From "+ str(receiver) + " get " + repr(data))
			time.sleep(1)


	'''
	Receive data from seeder
	'''
	def receivefromseeder(self):
		# Loop, printing any data we receive
		# self.socket.listen(5)

		# (reqSocket, (ip, port, key, scope_id)) =  self.socket.accept()
		#-----------------------------------
		# group will receive group ip and seeders ip from trackers.
		# now group will create TCP connection with seeders
		# and group will create UDP connection with its childs.


		while True:
			print "waiting to receive..."
			data, sender = self.socket.recvfrom(1500)
			while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
			print ("From "+ str(sender) + ' received ' + repr(data))
			print "Sending ack to: ", sender
			self.socket.sendto('ack', sender)




	'''
	Function for listening to childs and receiving the required piece from seeders.
	'''
	# group will open its UDP connection always.
	# whenever a leecher requests for a piece it will request to the group and group will then request the same piece 
	# with seeder and seeder will send the requested piece.
	def childrequest:
		# created a UDP socket
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		HOST  = ''
		PORT = 9999
		s.bind(HOST,PORT)
		while 1:
    # receive data from client (data, addr)
   d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
     
    reply = 'OK...' + data
     
    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     
s.close()


	