#!/usr/bin/python

import socket
from leecher import *


def main():
	
	print "Do something here"

	# Create the leecher's instance
	leecher = Leecher('124.0.0.2', 3555)

	# Download a torrent file form a server
	serverAddr = ('125.0.0.3', 1234)
	leecher.GetTorrent(serverAddr, "test.txt")



if __name__ == "__main__":
	main()