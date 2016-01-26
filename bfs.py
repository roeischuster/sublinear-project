'''
@created 25.01.2016

@author: crazy gangster
'''


NEIGHBOURHOOD_RADIUS = 5

def bfs_step(g, node_set):
	author_lists_sum = set() #just expand to all immediate neighbours of the nodes in the set
	for l in [g.authors[x].edges.keys() for x in node_set]:
		author_lists_sum.update(l) # use "update()" which works in-place (as opposed to union())
	return author_lists_sum 

def bfs(g, radius, initial_node):
	current = set([initial_node])
	traversed = set()
	for i in range(radius):
		result_step = bfs_step(g, current) #each step we expand the neighbourhood by 1.
		traversed = traversed.union(current)
		current = set([u for u in result_step if u not in traversed])

	return set.union(traversed, current)

