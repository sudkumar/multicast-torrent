#!/usr/bin/ python

from tracker import Tracker

def main():
	ip = '123.12.34.12'
	port = 5566
	dbName = 'tracker'

	tracker = Tracker(ip, port, dbName)

	tracker.Start()

if __name__=="__main__":
	main()