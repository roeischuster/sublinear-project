'''
Created on 18 Jan 2016

@author: Moshe
'''
import networkx as nx
import author
import graph

AUTHORS_FILE = "AMiner-Author.txt"
COAUTHS_FILE = "AMiner-Coauthor.txt"

def load_graph():
	g = graph.Graph()
	load_nodes(g)
	load_edges(g)
	return g

def load_nodes(graph):
	with open(AUTHORS_FILE,'r') as f:		
		line = f.readline()
		while line != "":
			
			line = line[len("#index "):]		# remove index prefix from line
			a_id = line.strip()					# 1st line (stripped) is author's index
			line = f.readline()					# read next line
			line = line[len("#n "):]			# remove name prefix from line
			if line.strip() == "":				# make sure name isn't empty
				line = "<empty_" + a_id + ">"
			name = line.strip()					# 2nd line (stripped) is author's name

			auth = author.Author(int(a_id), name)	# create author and
			graph.add_node(auth)				# add it to the graph

			#if graph.number_of_nodes() % 100000 == 0:
			#	print graph.number_of_nodes()
			
			while line.strip() != "":			# ignore additional author details and read next line
				line = f.readline()
			line = f.readline()

def load_edges(graph):
	with open(COAUTHS_FILE,'r') as f:			# load edges from coauthors file
		line = f.readline()
		while line != "":
			line = line[1:].split()				# remove '#' at the start of each line and split to fields
			w = int(line[2])					# 3rd field is weight, convert to int
			graph.add_edge(int(line[0]), int(line[1]), w)	# edge from auth1 to auth2
			line = f.readline()					# read next line
