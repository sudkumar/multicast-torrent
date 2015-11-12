#!/usr/bin/ python

from tracker import Tracker

def main():
	ip = '127.12.234.12'
	port = 7878
	dbName = 'trackers'

	tracker = Tracker(ip, port, dbName)

	tracker.Start()

if __name__=="__main__":
	main()