#!/usr/bin/ python

import socket


"""
Basic socket implementation
"""



class Socket():
	"""Basic Socket operations"""
	def __init__(self, ip, port=None):
		self.ip = ip
		self.port = port

	# get addr info	
	def GetAddr(self):
		return socket.getaddrinfo(self.ip, self.port, socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)[0]

	# create a TCP socket
	def TCP(self):
		# get the addr info 
		addrinfo = self.GetAddr()
		
		# get tcp IPv4 socket
		s = socket.socket(addrinfo[0], addrinfo[1], addrinfo[2])
		return s

	# create an UDP socket
	def UDP(self):
		addrinfo = socket.getaddrinfo(self.ip, self.port)[0]
		
		# create a UDP IPv4 socket
		s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

		return s

			
