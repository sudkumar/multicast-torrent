#!/usr/bin/python

import threading


class ClientThread(threading.Thread):
	def __init__(self, socket, ip, port):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket

	## implement the run functionality of thread 
	def run(self):
		# do the work here