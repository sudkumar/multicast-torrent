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
		self.socket.send("Ok")
		data = self.socket.recv(1024)
		if data == "Download" :
			self.socket.send("Ok")
			fileName = self.socket.recv(1024)
			print "User wants to download file "+ fileName
			self.Download(fileName)

		elif data == "Upload":
			print "User wants to upload file."
			# send confirmation
			self.socket.send("Ok")

			# get torrent file content
			print "Getting torrent file from seeder..."
			torrentFile = self.socket.recv(1024)
			
			# upload the file to server and do other necessary work
			self.Upload(torrentFile)

		else:
			print "Something went wrong"

		# now close the connection
		self.socket.close()


	"""
	Let client upload file to server
	"""
	def Upload(self, torrentFile):
		# decode the torrent file
		decod = Torrent().decode(torrentFile)

		# get the file name
		fileName = decod["info"]["name"]

		# get trackers 
		trackers = decod["announce"]

		# update database of itself
		print "Updating database of torrent files"
		self.server.db.torrents.insert({"fileName": fileName})

		# inform trackers to update there database
		trackerIP, trackerPort = trackers.split(":")
		trackerPort = int(trackerPort)

		print "Connecting to tracker at "+trackers
		serSoc = Socket('172.34.12.12', 6767).TCP()
		serSoc.connect((trackerIP, trackerPort))

		print "Waiting for response from racker"
		resp = serSoc.recv(256)
		if resp == "Ok":
			serSoc.send("Server")
			resp = serSoc.recv(256)
			if resp == "Ok":
				data = self.ip + ":" + str(self.port) + "||" + fileName
				print "Sending data to tracker..."
				serSoc.send(data)
				resp = serSoc.recv(256)
				if resp == "Failed":
					self.socket.send("Failed")
					return 
		else:
			self.socket.send("Failed")
			return

		# put file into the server 
		print "Putting content into a torrent file..."
		fp = open(fileName+".torrent", "wb")
		fp.write(torrentFile)
		fp.close()

		# send confirmation to client thread
		print "Sending confirmation to seeder..."
		serSoc.close()
		self.socket.send("Ok")
		return 

	"""
	Let client download file from server
	"""		
	def Download(self, fileName):
		# look in our data base for fileName, 
		files = self.server.db.torrents.find({"fileName": fileName})
		# send file if exists
		if files.count() >= 1:
			self.socket.send("Ok")
			torrentFile = open(fileName+".torrent", "rb")
			self.socket.send(torrentFile.read(1024))	

		# else send file not exists error
		else:
			self.socket.send("No")

class Server():
	"""Server for torrent files"""
	def __init__(self, ip, port=None, dbName=None):
		self.socket = None
		self.ip = ip
		self.port = port
		self.db = DB(dbName).db

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
