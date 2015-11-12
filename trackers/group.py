#!/usr/bin/ python

import socket
import time
import struct

# if __name__ == '__main__':
if __package__ is None:
  import sys
  from os import path
  sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
  from helpers.soc import Socket

else:
  from ..helpers.soc import Socket

"""
Group File (This will get created by trackers)

- Get data from seeders
	- Respond to leechers' request
	- If there is no leecher request for a finite time, suicide
"""




class Group():
	def __init__(self, ip=None, port=None, seeders=None, trackerAddr=None, ttl=1):
		if not (ip or port or seeders or trackerAddr) :
			print "Group required IP and port and seeders list"
			exit()

		self.trackerAddr = trackerAddr
		self.seeders = seeders
		# create a UDP socket
		print "Creating UDP group socket..."
		s1 = Socket(ip,port).UDP()
		
		# Set Time-to-live (optional)
		ttl_str = struct.pack('@i', ttl)

		# include ttl into IP header
		s1.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_str)
		
		# for udp
		# assign variable to group self
		self.gSocket = s1
		self.ip = ip
		self.port= port
		self.ttl = ttl
		self.gSocket.bind((ip, port))

		## for tcp
		port2 = 8982
		print "Creating TCP socket for seeder connection..."
		s2 = Socket(ip,port2).TCP()
		self.sSocket = s2
		self.port2 = port2
		self.sSocket.bind((ip, port2))
		print "Connecting to seeder ", seeders
		self.sSocket.connect(seeders)
		self.receivefromseeder()


	'''
	Receive data from seeder
	'''
	def receivefromseeder(self):
		# now group will create TCP connection with seeders
		# and group will create UDP connection with its childs.
		print "Waiting for connection from seeder..."
		resp = self.sSocket.recv(256)
		if resp == "Ok":
			self.sSocket.send("Group")
			resp = self.sSocket.recv(256)
			if resp == "Ok":
				# while True:					
				# get data from seeder
				data  = self.sSocket.recv(1024)

				# send data to leecher
				self.gSocket.sendto(data, (self.ip, self.port))

				print "Data is been delievered. Closing group."
				# close the group socket
				self.gSocket.close()
				self.sSocket.close()

				# connect to tracker and send him a request to remove this group
				self.Die()
				

			else:
				print "Seeder don't want any group to connect.."
		else:
			print "No response from seeder. Retry in 5 seconds."
			time.sleep(5)
			self.receivefromseeder()

		return

	"""
	Die
	"""
	def Die(self):
		s = Socket(self.ip, self.port2).TCP()
		s.connect(self.trackerAddr)
		resp = s.recv(256)
		if resp == "Ok":
			# send seederAddr and groupAddr to tracker.
			seederAddr = self.seeders[0] + ":" + str(self.seeders[1])
			groupAddr = self.ip + ":" + str(self.port)
			s.send(seederAddr + "||" + groupAddr)
			s.close()
			print "Group died successfully."
		else:
			print "Unable to remove group trackers database. Trying again"
			s.close()
		return 