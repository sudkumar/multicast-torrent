#!/usr/bin/ python

import socket
import time

"""
Group File (This will get created by trackers)

- Get data from seeders
	- Respond to leechers' request
	- If there is no leecher request for a finite time, suicide
"""


class Group():

	def __init__(self, ip=None, port=None, ttl=1):
		if not (groupIP or port) :
			print "Group required IP and port"
			exit()

		addrinfo = socket.getaddrinfo(ip, None)[0]
		# create a UDP socket with got family addrinfo[0]
		s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

		# Set Time-to-live (optional)
		ttl_str = struct.pack('@i', ttl)

		# include ttl into IP header
		s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_str)

		# assign variable to group self
		self.socket = s
		self.ip = ip
		self.port = port
		self.ttl = ttl
		self.socket.bind(ip, port)

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
	Receive data
	'''
	def receive(self):
		# Loop, printing any data we receive
		while True:
			print "waiting to receive..."
			data, sender = self.socket.recvfrom(1500)
			while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
			print ("From "+ str(sender) + ' received ' + repr(data))
			print "Sending ack to: ", sender
			self.socket.sendto('ack', sender)

