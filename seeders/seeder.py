#!/usr/bin/python
import socket
from ../helpers/torrent import *
"""
Seeders

- Upload .torrent file to server
- Get message from tracker for any download
	- Get group ip from tracker
	- Send file to group
"""
class ClientThread(threading.Thread):
	def __init__(self, socket, ip, port):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket

	## implement the run functionality of thread 
	def run(self):
		# get data from client socket
		if (groupSocket.recv(1024) == 'ok'):
			if (groupSocket.recv(1024) == 'group'):
				f = open(file_name, 'rb')
				l = f.read(1024)
				while(l):
					groupSocket.send(l)
					l = f.read(1024)
				f.close()
			else: 
				groupSocket.send('Error: Not a Group..')

		


class Seeder():
	"""Seeder for torrent file"""
	def __init__(self, ip, port):
		# ip, port
		self.ip = ip
		self.port = port
	
	"""
	Upload a torrent file
	"""
	def UploadTorrent(self, file_name, serverAddr):
		# create a tcp 
		s = lib.createTCP(self.ip, self.port)
		
		# connect to severAddr
		s.connect(serverAddr[0], serverAddr[1])
		s.send('seeder')
		# convert file to .torrent file
		a = torrent.Torrent(file_name)
		a.encode()
		s.send(file_name+'.torrent')

		# send torrent file to server
			# open the file
			# send recursively
		f = open(file_name+'.torrent', 'rb')
		l = f.read(1024)
		while(l):
			s.send(l)
			l = f.read(1024)
		f.close()

		# get response from server
		msg = s.recv(1024)
		if(msg == 'OK'):
			self.getGroup(s, file_name)
		else:
			s.close()
			self.UploadTorrent(file_name, serverAddr)
		
	"""
	Do message with Tracker and get the group IP 
	"""
	def GetGroup(self, sock, file_name):

		# keep connection open, listen
		sock.socket.listen(5)

		# accept connection from tracker
		while True:
			(groupSocket, (ip, port, key, scope_id)) = sock.socket.accept()
			groupSocket.send('connected')
			groupThread = ClientThread(groupSocket, ip, port)
			groupThread.start()
		# receive data from tracker, groupAddr

	# """
	# Send a file tp a group
	# """
	# def SendFile(self, groupSocket, file_name):
	# 	# create a TCP socket - no need
	# 	if (groupSocket.recv(1024) == 'ok'):
	# 		if (groupSocket.recv(1024) == 'group'):
	# 			f = open(file_name, 'rb')
	# 			l = f.read(1024)
	# 			while(l):
	# 				groupSocket.send(l)
	# 				l = f.read(1024)
	# 			f.close()
	# 		else: 
	# 			groupSocket.send('Error: Not a Group..')

	# 	groupSocket.close()

		# listen for group connection and responed it's request


