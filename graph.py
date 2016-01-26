'''
Created on 18 Jan 2016

@author: Moshe
'''

class Graph:
	def __init__(self):
		self.authors = {}
		self.edges = []
	
	def add_node(self,auth):
		self.authors[auth.id] = auth
		auth.edges = {}
	
	def add_edge(self,id1,id2,w=1):
		if not id2 in self.authors[id1].edges:
			self.authors[id1].edges[id2] = 0
		self.authors[id1].edges[id2] = w
		
		if not id1 in self.authors[id2].edges:
			self.authors[id2].edges[id1] = 0
		self.authors[id2].edges[id1] = w

		self.edges.append((id1,id2,w))
	
	def number_of_nodes(self):
		return len(self.authors)
	def number_of_edges(self):
		return len(self.edges)
	def number_of_isolated(self):
		i = 0
		for auth in self.authors.itervalues():
			if len(auth.edges) == 0:
				i += 1
		return i
