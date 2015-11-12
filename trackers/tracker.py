#!/usr/bin/ python

from group import Group
import threading

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
			print "Client is server. Responding to server..."
			# client is server, server wants to update our database
			self.socket.send("Ok")
			# now get the seeder and file from server
			resp = self.socket.recv(1024)
			seeder, fileName = resp.split("||")

			# update the collection of seeders
			# send the feedback to the server
			print "Updating database for seeders..."
			if self.tracker.db.seeders.insert({"seeder": seeder, "fileName": fileName}):
				self.socket.send("Ok")
			else:
				self.socket.send("Failed")	

		elif resp == "Leecher":
			print "Client is leecher. Responding to leecher..."
			# client is leecher, leecher wants to download a file with the filename
			self.socket.send("Ok")
			fileName = self.socket.recv(1024)
			timeToChat = (time.time() - startTime) * 1000
			print timeToChat, "ms"
			# round to 4 numbers to time
			timeToChat = "%.4f" % timeToChat
			print "Checking for file to exists in tracker's database..."
			file = self.tracker.db.seeders.find({"fileName": fileName})
			if file.count() >= 1:
				# send the confirmation to leecher
				self.socket.send("Ok")
				# file exists, so assign a group to the leecher 
				seederAddr = file[0]["seeder"]
				print seederAddr
				seederIP, seederPort = seederAddr.split(":")
				seederIP = str(seederIP)
				seederPort = int(seederPort)
				# check for any group in seeders list for with the same timeToChat
				print "Assinging group address to the leecher.."
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
							groupIP = '123.45.45.65'
							groupPort = 4343
							groupAddr = groupIP + ":" + str(groupPort) 
							
							group = Group(groupIP, groupPort, (seederIP, seederPort), (self.tracker.ip, self.tracker.port))

							# update the dictionary of seeders
							self.tracker.groups[seederAddr].append(groupAddr)
							self.tracker.groups[seederAddr].append(timeToChat)

				else:
					# there is not group of this seeder to send
					groupIP = '123.45.45.65'
					groupPort = 4343
					groupAddr = groupIP + ":" + str(groupPort) 
					group = Group(groupIP, groupPort, (seederIP, seederPort), (self.tracker.ip, self.tracker.port))
					self.tracker.groups[seederAddr] = [groupAddr, timeToChat]
				
				# send this group to leecher
				self.socket.send(groupAddr) 

			else:
				self.socket.send("File not exists in tracker's database...")
		
		elif resp == "Group":
			self.socket.send("Ok")
			# get seederAddr, groupAddr
			seederAddr, groupAddr = self.socket.recv(1024).split('||')
			if seederAddr in self.tracker.groups:
				itemLength = len(self.tracker.groups[seederAddr])
				for i in range(itemLength):
					val = self.tracker.groups[seederAddr][i]
					if val == groupAddr:
						# remove the group from seeders list
						self.tracker.groups[seederAddr].pop(i)
						self.tracker.groups[seederAddr].pop(i+1)

						# remove seeder if no more groups are active to this seeder
						if len(self.tracker.groups[seederAddr]) == 0:
							self.tracker.groups.pop(seederAdd)

						break
		
		else:
			self.socket.send("Who are you ?")
		
		self.socket.close()

class Tracker():
	"""Tracker for torrents"""
	def __init__(self, ip, port=None, dbName=None):
		self.ip = ip
		self.port = port
		if dbName:
			self.db = DB(dbName).db
		else:
			self.db = None

		self.socket = None
		self.groups = {}

	# start the tracker server	
	def Start(self):
		# create a tcp thread
		self.socket = Socket(self.ip, self.port).TCP()
		self.socket.bind((self.ip, self.port))

		# now listen for any incomming connection
		print "Tracker listening at  "+ self.ip + ":"+str(self.port)
		self.socket.listen(5)

		while True:
			clientSocket, (ip, port) = self.socket.accept()
			print "Responding to ", ip, port
			clientThread = ClientThread(self, clientSocket, ip, port)
			clientThread.start()


