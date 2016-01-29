import pickle
DECAY = 0.8

cache = {}
def return_and_cache(element, val):
	cache[element] = val
	return val

def recursive_stupid_wsimrank(g, node1, node2, t):
	#print "%d %d %d"%(node1, node2, t)
	if node1 == node2:
		return 1
	if t == 0:
		return 0
	if (node1, node2, t) in cache.keys():
		return cache[(node1, node2, t)]
	if (node2 not in pickle.load(open("neighbourhood/%s"%node1, 'rb'))):
		return return_and_cache((node1, node2, t), 0)
	
	neighbours1 = g.authors[node1].edges
	neighbours2 = g.authors[node2].edges

	neighbours_mult = [neighbours1[i]*neighbours2[j] for i in neighbours1.keys() for j in neighbours2.keys()]

	simrank_sum = sum([mult*recursive_stupid_wsimrank(g, i, j, t-1) for mult in neighbours_mult])
	normalize = sum(neighbours_mult)

	return return_and_cache((node1, node2, t), (DECAY/normalize)*simrank_sum)


def weighted_simrank(g, subgraph_nodes):
	#simranks = {(node, node):1 for node in g.authors.keys()} #simrank shall contain the weighted simrank, only where it's not 0, so access should always be via simranks.get((x,y),0)
	print recursive_stupid_wsimrank(g, list(subgraph_nodes)[1], list(subgraph_nodes)[2], 3)

	

def read_neighbours(g):
	i = 0
	for auth_id, auth in g.authors.iteritems():
		auth.neighbours = pickle.load(open("neighbourhood/%s"%auth_id, 'rb'))
		if (i % 500) == 0:
			print "reading neighbours, iteration %d out of %d"%(i, len(g.authors))
		i += 1
