#!/usr/bin/python

import socket
import struct

if __package__ is None:
  import sys
  from os import path
  sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
  from helpers.soc import Socket
  from helpers.torrent import Torrent

else:
  from ..helpers.soc import Socket
  from ..helpers.torrent import Torrent



"""
Leechers

- Download a .torrent file and decode it
	- Do some messaging with trackers and get group ip
		- join the group ang get file   
"""


class Leecher():
	"""Leecher to download the file"""
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

	"""
	Download torrent file
	"""
	def GetTorrent(self, serverAddress, fileName):
		'''
		Create a TCP socket
		Connect the server
		Get the torrent file from server
		'''
		print "Downloading "+ fileName
		# Create a TCP socket
		s = Socket(self.ip, self.port).TCP()

		# connect to server
		print "Connecting to ", serverAddress
		# s.settimeout(5)   # 5 seconds
		try:
		    s.connect(serverAddress)         # "random" IP address and port
		except socket.error, exc:
		    print "Caught exception socket.error : %s" % exc
		else:
			# get torrent file from server after some message passing
			resp = s.recv(256)
			if resp == "Ok":
				s.send("Download")
				resp = s.recv(256)
				if resp == "Ok":
					s.send(fileName)
					resp = s.recv(256)
					if resp == "Ok":
						fileContent = s.recv(1024)
						fp = open(fileName+".torrent", "w")
						fp.write(fileContent)
						fp.close()
					else:
						print "File not exists at server"	

			else:
				print "Server not respoinding..."
		# close the socket
		s.close()			
	

	"""
	Talk to Trackers and get the group 
	"""
	def GetGroup(self, trackerAddr, fileName):
		'''
		Get tracker's ip and port
		Create a TCP socket and get group after doing some message passing
		'''					
		# create a tcp socket
		s = Socket(self.ip, self.port).TCP()

		s.bind((self.ip, self.port))
		
		# connect socket to tracker
		s.connect(trackerAddr)

		# get group from tracker after doing some message passing
		resp = s.recv(256)
		if resp == "Ok":
			s.send("Leecher")
			resp = s.recv(256)
			if resp == "Ok":
				s.send(fileName)
				resp = s.recv(256)
				if resp == "Ok":
					resp = s.recv(1024)
					if resp == "Failed":
						print "Unable to assign a group.."
						groupAddr =  None
					# we got the group addr	
					groupAddr = resp
				else:
					print "File not exists at server"
					groupAddr = None
		else:
			print "Tracker is not respoinding..."
			groupAddr =  None		
		
		s.close()

		return groupAddr

	"""
	Join the group
	"""
	def JoinGroup(self, groupIP, groupPort):
		'''
		Create a UDP socket
		Join the group
		'''

		s = Socket(self.ip, self.port).UDP()

		# Allow multiple copies of this program on one machine
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


		# Bind it to the port
		s.bind((groupIP, groupPort))

		# get the group to join
		group_bin = socket.inet_pton(socket.AF_INET, groupIP)

		# Join group
		mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	
		return s


	"""
	Download a file
	"""
	def Download(self, torrentFile):
		# get the trackers from torrent file
		fp = open(torrentFile, "rb")
		encodedData = fp.read(1024)
		fp.close()
		decodedData = Torrent().decode(encodedData)

		# get the tracker from dictionary
		tracker = decodedData["announce"].split(':')
		
		fileName = decodedData["info"]["name"]
		
		# get the group to join
		trackerAddr = ( tracker[0], int(tracker[1]) )

		groupAddr = self.GetGroup(trackerAddr, fileName)
		if groupAddr:	
			groupIP, groupPort = groupAddr.split(':')

			# join the group and get the socket
			s = self.JoinGroup(str(groupIP), int(groupPort))

			# Loop, printing any data we receive
			while True:
				print "waiting to receive..."
				data, sender = s.recvfrom(1500)
				print ("From "+ str(sender) + ' received ' + repr(data))
				print "Sending ack to: ", sender
				s.sendto('ack', sender)
