# Multi-cast Bit-torrent Implementation

## Functionality
> This is a simple torrent implementation on multi-cast. We have used response time from leecher to form there multi-cast group. Group management is done by trackers. Leechers with same response time and of same file will be kept the same group. MongoDB database is used. 

## Work flow

#### Uploading 
* Seeder will first upload a .torrent file to the server. 
* Server will decode the file and will get the trackers list. After that server will start a communication with trackers and will ask them to update there database for new file by adding seeder-file tuple. Server will also keep the file and will also update it's database.

#### Downloading .torrent file
* Leecher will first ask the server for a file.
* If file found, server will let leecher download the file.

#### Downloading file
* Leecher will decode the torrent file and will extract the trackers list. After this, leecher will make connection with trackers.
* Now tracker will do some message passing with leecher and will get seeder from it's database for the requested file. After doing some message passing, tracker will create some sockets and will assign them to leechers. These sockets are groups. 
* Now each leecher will join the group and will wait for any data to receive.
* On the other hand, groups will connect to seeder by getting there IPs from tracker and will get data from seeder and will deliver data to each leecher.
* When done, group will kill himself, and will inform tracker about itself.

## File structure

> Each directory represents it's own functionality.

## Running 

> To start server

	cd servers
	python serve.py

> To start trackers

	cd trackers
	python track.py

> To upload a file

	cd seeders
	python seed.py

> To download a torrent file

	cd leechers
	python run.py

> To download a file as leecher

Make sure that seeder is seeding ( do into seeders/seed.py and uncomment the sendfile function). And also make sure that from  leechers/run.py, download function is uncommented.
	
	cd leechers
	python run.py






