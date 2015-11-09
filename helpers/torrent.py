#!/usr/bin/ python

"""
Torrent-File handler

- Encoding a given file and creating a torrent file 
- Decoding a torrent file and returning it's decoded dictionary
"""

import bencode
from hashlib import sha1
import base64
import os

# print bdecode(open('[kat.cr]the.snow.queen.2.2015.hdrip.xvid.ac3.evo.torrent', 'rb').read())

class Torrent():

	def __init__(self, fileName=None):
		if not fileName:
			print "Please provide a file"
			exit()	
		self.fileName = fileName

	''' create torrent file with given parameters '''
	def encode(self, announce="http://localhost:80/torrent", groupIP="225.0.0.0", pieceSize=26214):
		
		# variable to contain number of pieces for fileName
		piecesString = ""
		# open file in binary mode
		f = open(self.fileName, 'rb')
		while True:
			piece = f.read(pieceSize)
			if not piece:
				break
			# 20 bytes sha1
			piecesString += sha1(piece).digest()

		# get the length of the file 	
		length  = os.path.getsize(fileName)

		# make dictionary for encoding
		dbecode = {
			'announce': announce, 
			'groupIP': groupIP, 
			'info': {
				'name': fileName, 
				'piece length': pieceSize, 
				'length': length, 
				'pieces': piecesString
			}
		}

		# make encoded string
		bencodedString =  bencode.bencode(dbecode)
		
		# create file for this encoded torrent data
		f = open(self.fileName+".torrent", 'wb')
		f.write(bencodedString)
		f.close()	

	''' decode torrent file and return it"s content '''
	def decode(self):
		f = open(self.fileName, 'rb')
		bencodeString = f.read()
		f.close()
		bdecode = bencode.bdecode(bencodeString)

		# return the decoded dictionary
		return bdecode
