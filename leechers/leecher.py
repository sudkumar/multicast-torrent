#!/usr/bin/python

import socket

"""
Leechers

- Download a .torrent file and decode it
	- Do some messaging with trackers and get group ip
		- join the group ang get file   
"""


class Leecher():
	"""Leecher to download the file"""
	def __init__(self, ip, port):
		addrinfo = socket.getaddrinfo(ip, None)[0]

		s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

		# Allow multiple copies of this program on one machine
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.socket = s
		self.ip = ip
		self.port = port
		self.socket.bind(ip,port)

	"""
	Download torrent file
	"""
	def GetTorrent(self, serverAddress):
		# to download a file, we want a TCP connection
		# create a TCP socket and connect to server address
		# do some message passing and then get file from server

	"""
	Talk to Trackers and get the group 
	"""
	def GetGroup(self):
			

	"""
	Join the group
	"""
	def JoinGroup(self, group):
		
		# Bind it to the port
		self.socket.bind((group.ip, group.port))

		# get the group to join
		group_bin = socket.inet_pton(group.socket.family, group.ip)

		# Join group
		mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


	"""
	Download a file
	"""
	def Download(self):
		# Loop, printing any data we receive
		while True:
			print "waiting to receive..."
			data, sender = self.socket.recvfrom(1500)
			while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
			print ("From "+ str(sender) + ' received ' + repr(data))
			print "Sending ack to: ", sender
			s.sendto('ack', sender)