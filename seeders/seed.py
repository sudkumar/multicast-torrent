#!/usr/bin/ python

from seeder import Seeder



def main():
	ip = '127.12.123.12'
	port = 5543

	seeder  = Seeder(ip, port)

	serverAddr = ('127.23.23.23', 6660)

	# seeder.UploadTorrent('test.txt', serverAddr)

	seeder.SendFile('test.txt')

if __name__ == "__main__":
	main()