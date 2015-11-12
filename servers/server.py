#!/usr/bin/ python

import threading
import socket

if __package__ is None:
  import sys
  from os import path
  sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
  from helpers.soc import Socket
  from helpers.torrent import Torrent
  from helpers.db import DB

else:
  from ..helpers.soc import Socket
  from ..helpers.torrent import Torrent
  from ..helpers.db import DB


"""
Torrent Server

- Get .torrent file from seeder
	- Inform trackers about the .torrent file
- Let leechers download the torrent file
"""
class ClientThread(threading.Thread):
	def __init__(self, server, socket, ip, port):
		threading.Thread.__init__(self)
		self.server = server
		self.ip = ip
		self.port = port
		self.socket = socket

	## implement the run functionality of thread 
	def run(self):
		# get data from client socket
		data = self.socket.recv(1024)
		if data == "Download" :
			self.socket.send("Ok")
			fileName = self.socket.recv(1024)
			self.Download(fileName)

		elif data == "Upload":
			# send confirmation
			self.socket.send("Ok")

			# get torrent file content
			torrentFile = self.socket.recv(1024)
			
			# upload the file to server and do other necessary work
			self.server.Upload(torrentFile)

		else:
			print "Something went wrong"

		# now close the connection
		self.socket.close()


	"""
	Let client upload file to server
	"""
	def Upload(self, torrentFile):
		# decode the torrent file
		decod = Torrent.decode(torrentFile)

		# get the file name
		fileName = decod["info"]["name"]

		# get trackers 
		trackers = decod["announce"]

		# update database of itself
		self.server.db.insert({"fileName": fileName+".torrent"})

		# inform trackers to update there database
		trackerIP, trackerPort = trackers.split(":")

		serSoc = self.server.socket
		serSoc.connect((trackerIP, trackerPort))
		resp = serSoc.recv(256)
		if resp == "Ok":
			serSoc.send("Server")
			resp = serSoc.recv(256)
			if resp == "Ok":
				data = self.ip + ":" + self.port + "||" + fileName
				serSoc.send(data)
				resp = serSoc.revc(256)
				if resp == "Failed":
					self.socket.send("Failed")
					return 
		else:
			self.socket.send("File upload failed!!")
			return

		# put file into the server 
		fp = open(fileName+".torrent", "wb")
		fp.write(torrentFile)
		fp.close()

		# send confirmation to client thread
		self.socket.send("Done")
		return 

	"""
	Let client download file from server
	"""		
	def Download(self, fileName):
		# look in our data base for fileName, 
		file = self.server.db.find({"fileName": fileName})

		# send file if exists
		if file:
			torrentFile = open(fileName, "rb")
			self.socket.send(torrentFile)	

		# else send file not exists error
		else:
			self.socket.send("No")

class Server():
	"""Server for torrent files"""
	def __init__(self, ip, port=None, dbName=None):
		self.socket = None
		self.ip = ip
		self.port = port
		self.db = DB(dbName)

	"""
	Start the server
	"""
	def Start(self):
		# create a tcp socket	
		self.socket = Socket(self.ip, self.port).TCP()
		self.socket.bind((self.ip, self.port))

		# listen for any incomming connections
		print "Listening at: ", (self.ip, self.port)
		self.socket.listen(5)

		while True:
			clientSocket, (ip, port) = self.socket.accept()
			print "Responding to : ", ip, port
			clientThread = ClientThread(self, clientSocket, ip, port)
			clientThread.start()
