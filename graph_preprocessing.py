#!/usr/bin/python

'''
@created 26.01.2016 (Austrlia day 2016)

@author crazy penguin
'''

import loader
import bfs
import pickle

def bound_degree(g, degree):
	'''
	remove all nodes in g with degree >= "degree"
	todo: we don't remove the edges from g.edges, because they're never used. 
	todo: this should probably be in "graph.py"
	'''
	authors_to_remove = []

	for auth in g.authors.keys():
	    if len(g.authors[auth].edges) >= degree:
                authors_to_remove.append(auth)

	print "removing %d authors"%len(authors_to_remove)

	iteration = 0
	for auth_id, auth in g.authors.iteritems():
		if (iteration % 10000 == 0):
			print "bounding degree, %f % done"%(100*float(iteration)/len(g.authors))
		iteration +=1

		l = auth.edges
		s = set.intersection(set(l.keys()), set(authors_to_remove))
		for to_remove in s:
			l.pop(to_remove)

def neighbourhood_all(g, depth):
	'''
	set neighbourhood of each node to BFS of depth "depth"
	todo: this should probably be in "graph.py"
	'''
	iteration = 0
	for auth_id, auth_t in g.authors.iteritems():
		if (iteration%1000 == 0):
			print "computing neighbourhood %d out of %d"%(iteration, len(g.authors))
		iteration += 1
		pickle.dump(bfs.bfs(g, depth, auth_id), open("neighbourhood/%d"%auth_id, 'wb'))


print "loading graph"
g = loader.load_graph()
print "bounding degree to %d"%50
bound_degree(g, 50)
print "saving bound-degree graph to file"
pickle.dump(g, open("processed_graph.pickle", "wb"))
print "setting neighbourhood for all nodes"
neighbourhood_all(g, 5)
print "done"
