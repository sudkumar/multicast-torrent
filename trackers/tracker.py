#!/usr/bin/ python

from group import Group
import threading
# from ...helpers.db import DB

import time

# if __name__ == '__main__':
if __package__ is None:
  import sys
  from os import path
  sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
  from helpers.db import DB
  from helpers.soc import Socket

else:
  from ..helpers.db import DB
  from ..helpers.soc import Socket


"""
Torrent Trackers

- Listen from server if there is any new file added with this tracker as in its announce list
	- Store .torrent file 
	- Update it's data set to include seeder-torrentFile tuple
- Listen from leechers for file
	- Create a groups of leechers by doing some message passing
		- Send these group ips to seeder 
"""
	


class ClientThread(threading.Thread):
	def __init__(self, tracker, socket, ip, port):
		threading.Thread.__init__(self)
		self.tracker = tracker
		self.ip = ip
		self.port = port
		self.socket = socket

	## implement the run functionality of thread 
	def run(self):
		# send  the confirmation to the client
		startTime = time.time()
		self.socket.send("Ok")

		# get the first message from client		
		resp = self.socket.recv(256)
		if resp == "Server":
			# client is server, server wants to update our database
			self.socket.send("Ok")
			# now get the seeder and file from server
			resp = self.socket.recv(1024)
			seeder, fileName = resp.split("||")

			# update the collection of seeders
			# send the feedback to the server
			if self.tracker.db.seeder.insert({"seeder": seeder, "fileName": fileName}):
				self.socket.send("Ok")
			else:
				self.socket.send("Failed")	

		elif resp == "Leecher":
			# client is leecher, leecher wants to download a file with the filename
			self.socket.send("Ok")
			fileName = self.socket.recv(1024)
			timeToChat = (time.time() - startTime) * 1000
			print timeToChat, "ms"
			# round to 4 numbers to time
			timeToChat = "%.4f" % timeToChat
			file = self.tracker.db.seeder.fild({"fileName": fileName})
			if file:
				# file exists, so assign a group to the leecher 
				seederAddr = file[0].seeder

				# check for any group in seeders list for with the same timeToChat
				if seederAddr in self.tracker.groups:
					itemLength = len(self.tracker.groups[seederAddr])
					for i in range(itemLength):
						val = self.tracker.groups[seederAddr][i]
						if val == timeToChat:
							# we have a group with the same time stamp, so assign this group to the leecher
							groupAddr = self.tracker.groups[seederAddr][i-1]
							break
						else:
							# group is not already present for this seeder
							# create a group with a ip of class D and port
							groupIP = '244.23.23.23'
							groupPort = 4343
							groupAddr = groupIP + ":" + str(groupPort) 
							group = Group(groupIP, groupPort, seederAddr, trackerAddr)

							# update the dictionary of seeders
							self.tracker.groups[seederAddr].append(groupAddr)
							self.tracker.groups[seederAddr].append(timeToChat)

				else:
					# there is not group of this seeder to send
					groupIP = '244.23.23.23'
					groupPort = 4343
					groupAddr = groupIP + ":" + str(groupPort) 
					group = Group(groupIP, groupPort, seederAddr, trackerAddr)
					self.tracker.groups[seederAddr] = [groupAddr, timeToChat]
				
				# send this group to leecher
				trackerAddr = self.tracker.ip + ":" +str(self.tracker.port)
				self.socket.send(groupAddr) 

			else:
				self.socket.send("File not exists in tracker's database...")
		
		elif resp == "Group":
			self.socket.send("Ok")
			# get seederAddr, groupAddr
			fileName = self.socket.recv(1024)
				
		
		else:
			self.socket.send("Who are you ?")
		
		self.socket.close()

class Tracker():
	"""Tracker for torrents"""
	def __init__(self, ip, port=None, dbName=None):
		self.ip = ip
		self.port = port
		if dbName:
			self.db = DB(dbName)
		else:
			self.db = None

		self.socket = None
		self.groups = {}

	# start the tracker server	
	def Start(self):
		# create a tcp thread
		s = Socket(self.ip, self.port).TCP()

		# now listen for any incomming connection
		self.socket = s
		self.socket.listen(5)

		print "Tracker listening at  "+ self.ip + ":"+str(self.port)

		while True:
			clientSocket, (ip, port, key, scope_id) = self.socket.accept()
			print "Client from "+ str(ip) + ":" + str(port)
			clientThread = ClientThread(self, clientSocket, ip, port)
			clientThread.start()


