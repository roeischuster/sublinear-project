'''
Created on 18 Jan 2016

@author: Moshe
'''

class Author:
	def __init__(self,a_id,name):
		self.id = a_id
		self.name = name
		self.edges = {}
		
	def __hash__(self):
		return int(self.id)
	def __eq__(self,auth):
		if isinstance(auth, basestring):
			return self.id == auth
		elif isinstance(auth, Author):
			return self.id == auth.id
		else:
			return False