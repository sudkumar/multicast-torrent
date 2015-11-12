#!/usr/bin/ python

from server import Server

"""
Server file to intialize out server
"""

def main():
	ip = '127.23.23.23'
	port = 6660
	# create server at a given ip, port and a database
	server = Server(ip, port, 'servers')
	server.Start()



if __name__ == "__main__":
	main()