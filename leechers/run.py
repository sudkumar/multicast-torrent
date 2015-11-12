#!/usr/bin/python

import socket
from leecher import *


def main():
	
	# Create the leecher's instance
	leecher = Leecher('127.100.11.11', 3555)

	# Download a torrent file form a server
	serverAddr = ('127.23.23.23', 6660)
	leecher.GetTorrent(serverAddr, "test.txt")



if __name__ == "__main__":
	main()