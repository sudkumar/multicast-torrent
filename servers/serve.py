#!/usr/bin/ python

from server import *

"""
Server file to intialize out server
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
		data = self.socket.recv(1024)

		# send data to client socket
		sent = self.socket.send("Send something to socket")



def main():
	
	# create server at a given ip and port
	server = Server(ip, port)

	# listen for connection
	server.socket.listen(5)

	while True:
		(clientSocket, (ip, port, key, scope_id)) = server.socket.accept()
		print "Client with " + ip + ":"+str(port) + " connected."
		clientSocket.send("Welcome to the server...")
		# now send the user to a thread
		clientThread = ClientThread( clientSocket, ip, port)
		clientThread.start()


if __name__ == "__main__":
	main()