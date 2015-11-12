#!/usr/bin/python

import threading

if __package__ is None:
  import sys
  from os import path
  sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
  from helpers.torrent import Torrent
  from helpers.soc import Socket

else:
  from ..helpers.torrent import Torrent
  from ..helpers.soc import Socket


"""
Seeders

- Upload .torrent file to server
- Get message from tracker for any download
	- Get group ip from tracker
	- Send file to group
"""
class ClientThread(threading.Thread):
	def __init__(self, socket, ip, port, file_name):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		self.file_name = file_name

	## implement the run functionality of thread 
	def run(self):
		# get data from client socket
		self.socket.send("Ok")
		resp = self.socket.recv(256)
		if (resp == "Group"):
			self.socket.send("Ok")
			f = open(self.file_name, 'rb')
			l = f.read(1024)
			self.socket.send(l)
			f.close()
			print "File successfully sent."
		else: 
			self.socket.send('Error: Not a Group..')


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
		s = Socket(self.ip, self.port).TCP()
		
		s.bind((self.ip, self.port))
		# connect to severAddr
		print "Connecting to :", serverAddr
		s.connect(serverAddr)
		
		# upload file to server
		resp = s.recv(256)
		if resp == "Ok":
			s.send("Upload")
			resp = s.recv(256)
			if resp == "Ok":
				# convert file to .torrent file
				print "Creating torrent file."
				fp = open(file_name, 'rb')
				fileContent = fp.read(1024)
				enCodedString = Torrent().encode(fileName=file_name)
				fp.close()
				
				fp = open(file_name+".torrent", "wb")
				fp.write(enCodedString)
				fp.close()

				# send torrent file to server
				# open the file
				# send recursively
				print "Sending file to server.."
				f = open(file_name+'.torrent', 'rb')
				l = f.read(1024)
				while(l):
					s.send(l)
					l = f.read(1024)
				f.close()

				print "Waiting for resonse from server"
				resp = s.recv(1024)
				if resp == "Failed":
					print "File upload failed."
					s.close()
					# self.UploadTorrent(file_name, serverAddr)
				elif resp == "Ok":
					# file successfully uploaded. Now open socket to let users download this file
					print "File successfully uploaded."
					s.close()
					self.SendFile( file_name)
			else:
				print "Server won't let you upload"
		else:
			print "Unable to talk to server. Please try after sometime."
			s.close()
			
		
	"""
	Do message with Tracker and get the group IP 
	"""
	def SendFile(self, file_name):

		print "Waiting for any group connection at ", self.ip, self.port, "..."
		# keep connection open, listen
		sock = Socket(self.ip, self.port).TCP()
		sock.bind((self.ip, self.port))
		sock.listen(5)

		# accept connection from tracker
		while True:
			groupSocket, (ip, port) = sock.accept()
			print "Seeding to group ", ip, port
			groupThread = ClientThread(groupSocket, ip, port, file_name)
			groupThread.start()

