#!/usr/bin/ python

from pymongo import MongoClient

class DB():
	"""DB for servers"""
	
	conn = MongoClient()

	def __init__(self, db):
		if not conn:
			conn = MongoClient()	
		else 
			conn = MongoClient(host, port)
		
		self.db = conn[db]