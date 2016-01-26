import pickle
DECAY = 0.4

def recursive_stupid_wsimrank(g, node1, node2, t):
	if node1 == node2:
		return 1
	if t == 0:
		return 0
	if (node2 not in pickle.load("neighbourhood/%s"%node1)):
		return 0

	
	neighbours1 = g.authors[node1].edges
	neighbours2 = g.authors[node2].edges

	simrank_sum = sum([[neighbours1[i]*neighbours2[j]*recursive_stupid_wsimrank(g, i, j, t-1) for i in neighbours1.keys() for j in neighbours2.keys()]])
	normalize = sum([[neighbours1[i]*neighbours2[j] for i in neighbours1.keys()] for j in neighbours2.keys()])

	return (DECAY/normalize)*simrank_sum


def weighted_simrank(g, subgraph_nodes)
	#simranks = {(node, node):1 for node in g.authors.keys()} #simrank shall contain the weighted simrank, only where it's not 0, so access should always be via simranks.get((x,y),0)
	print recursive_stupid_wsimrank(g, list(subgraph_nodes)[1], list(subgraph_nodes)[2], 3)

	

	
