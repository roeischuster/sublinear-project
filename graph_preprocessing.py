#!/usr/bin/python

'''
@created 26.01.2016 (Austrlia day 2016)

@author crazy penguin
'''

import loader
import bfs
import pickle


def remove_authors(g, authors_to_remove):
	'''
	helper method, removes all nodes in "authors_to_remove"
	todo: we don't remove the edges from g.edges, because they're never used. 
	'''
	print "removing %d authors"%len(authors_to_remove)
	iteration = 0

	for author in authors_to_remove:
		g.authors.pop(author)

	authors_to_remove_set = set(authors_to_remove)

	for auth_id, auth in g.authors.iteritems():
		if (iteration % 10000 == 0):
			print "removing %d authors, %f percent done"%(len(authors_to_remove_set), (100*float(iteration)/len(g.authors)))
		iteration +=1

		l = auth.edges
		intersection = [e for e in l.keys() if e in authors_to_remove_set] # don't use set() for efficiency concerns
		for to_remove in intersection:
			l.pop(to_remove)


def noga_alon_projection(g, depth):
	'''
	Remove all nodes in g that are not close enough to noga alon (see in code what is "close enough")
	Note that depth 4 ~= 400,000 nodes. depth 5 ~= 800,000. Higher than that seems to converge to ~1000000
	So, if we run with depth=4 we get a 400,000 node graph.
	todo: this should probably be in "graph.py"
	'''
	noga_id = 1653815 # he has other IDs, but this is clearly his primary one (with 330 cooperations as opposed to <10 for the rest)
	noga_projection = bfs.bfs(g, depth, noga_id) # 
	
	authors_to_remove = [author for author in g.authors.keys() if author not in noga_projection]

	remove_authors(g, authors_to_remove)
	

def bound_degree(g, degree):
	'''
	remove all nodes in g with degree >= "degree"
	todo: this should probably be in "graph.py"
	'''
	authors_to_remove = []

	for auth in g.authors.keys():
		if len(g.authors[auth].edges) >= degree:
			authors_to_remove.append(auth)

	remove_authors(g, authors_to_remove)

def remove_low_degree(g, degree):
	'''
	just like bound_degree, only removes low degrees (instead of high)
	remove all nodes in g with degree >= "degree"
	todo: this should probably be in "graph.py"
	'''
	authors_to_remove = []

	for auth in g.authors.keys():
		if len(g.authors[auth].edges) <= degree:
			authors_to_remove.append(auth)

	remove_authors(g, authors_to_remove)



def neighbourhood_all(g, depth):
	'''
	set neighbourhood of each node to BFS of depth "depth"
	todo: this should probably be in "graph.py"
	'''
	iteration = 0
	for auth_id, auth_t in g.authors.iteritems():
		if (iteration%250 == 0):
			print "computing neighbourhood %d out of %d"%(iteration, len(g.authors))
		iteration += 1
		pickle.dump(bfs.bfs(g, depth, auth_id), open("neighbourhood/%d"%auth_id, 'wb')) # we actually dump the neighbourhood to a file, can't save all of this in memory. It enables easy enough access from code, but not very efficient.


print "loading graph"
g = loader.load_graph()
print "noga alon projection"
noga_alon_projection(g, 3)
print "bounding degree to %d"%50
bound_degree(g, 50)
print "removing low degree nodes"
remove_low_degree(g, 3)
print "saving resultant graph to file"
pickle.dump(g, open("processed_graph.pickle", "wb"))
print "setting neighbourhood for all nodes"
neighbourhood_all(g, 3)
print "done"
