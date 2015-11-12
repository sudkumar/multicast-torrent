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

	''' create torrent file with given parameters '''
	def encode(self, fileName, announce="127.12.234.12:7878", pieceSize=26214):
		
		# variable to contain number of pieces for fileName
		piecesString = ""
		# open file in binary mode
		f = open(fileName, 'rb')
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
			'info': {
				'name': fileName, 
				'piece length': pieceSize, 
				'length': length, 
				'pieces': piecesString
			}
		}

		# make encoded string
		bencodedString =  bencode.bencode(dbecode)
		
		return bencodedString	

	''' decode torrent file and return it"s content '''
	def decode(self, bencodedString):
		bdecode = bencode.bdecode(bencodedString)
		# return the decoded dictionary
		return bdecode
