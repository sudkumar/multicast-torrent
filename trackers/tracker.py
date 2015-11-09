#!/usr/bin/ python

"""
Torrent Trackers

- Listen from server if there is any new file added with this tracker as in its announce list
	- Store .torrent file 
	- Update it's data set to include seeder-torrentFile tuple
- Listen from leechers for file
	- Create a groups of leechers by doing some message passing
		- Send these group ips to seeder 
"""