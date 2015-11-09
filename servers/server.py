#!/usr/bin/ python

"""
Torrent Server

- Get .torrent file from seeder
	- Inform trackers about the .torrent file
- Let leechers download the torrent file
"""

class Server():
	"""Server for torrent files"""
	def __init__(self, ip, port):
		# create a TCP IPv4 socket for server
		addrinfo = socket.getaddrinfo(ip, port, socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)[0]
		s = socket.socket(addrinfo[0], addrinfo[1], addrinfo[2])
		self.socket = s
		self.ip = ip
		self.port = port
		self.socket.bind(ip, port)

	"""
	Let upload file to server
	"""
	def Upload(self, file):


	"""
	Let download file from server
	"""		
	def Download(self, file):
		