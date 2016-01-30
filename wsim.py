import pickle
import time
DECAY = 0.95
DEPTH = 2

def init_cache(g):
	'''
	Initialize simrank cache for graph g
	'''
	g.cache = {}

def return_and_cache(g, element, val):
	'''
	Code (and function name) is pretty self explainatory here
	'''
	g.cache[element] = val
	return val

def simrank_impl(g, node1, node2, t, is_weighted):
	'''
	Weighted simrank implementation
	'''
	#print "%d %d %d"%(node1, node2, t)
	if node1 == node2:
		return 1
	if t == 0:
		return 0
	if (node1, node2, t) in g.cache.keys():
		return g.cache[(node1, node2, t)]
	#if (node2 not in pickle.load(open("neighbourhood/%s"%node1, 'rb'))):
	#if (node2 not in g.authors[node1].neighbours):
	#	return return_and_cache(g, (node1, node2, t), 0)
	
	neighbours1 = g.authors[node1].edges
	neighbours2 = g.authors[node2].edges

	if is_weighted:
		neighbours_mult = [(neighbours1[i]*neighbours2[j], i, j) for i in neighbours1.keys() for j in neighbours2.keys()]
	else:
		neighbours_mult = [(1, i, j) for i in neighbours1.keys() for j in neighbours2.keys()]
	

	simrank_sum = sum([mult*simrank_impl(g, i, j, t-1, is_weighted) for (mult, i, j) in neighbours_mult])
	normalize = sum([mult for (mult, i, j) in neighbours_mult])

	return return_and_cache(g, (node1, node2, t), (DECAY/normalize)*simrank_sum)

def simrank(g, node1, node2, depth=DEPTH):
	'''
	NON-weighted variant
	'''
	init_cache(g)
	start = time.time()
	res = simrank_impl(g, node1, node2, depth, False)
	end = time.time()
	print "simrank took %f seconds"%(end-start)
	return res

def wsimrank(g, node1, node2, depth=DEPTH):
	'''
	weighted variant
	'''
	init_cache(g)
	start = time.time()
	res = simrank_impl(g, node1, node2, depth, True)
	end = time.time()
	print "weighted simrank took %f seconds"%(end-start)
	return res



def read_neighbours(g):
	'''
	Read neighbours of all nodes from disk into memory.
	Neighbours are assumed to be stored under the "neighbours" directory.
	'''
	i = 0
	for auth_id, auth in g.authors.iteritems():
		auth.neighbours = pickle.load(open("neighbourhood/%s"%auth_id, 'rb'))
		if (i % 500) == 0:
			print "reading neighbours, iteration %d out of %d"%(i, len(g.authors))
		i += 1


def experiment_phaze1():
	print "loading graph"
	g =  pickle.load(open("processed_graph.pickle"))
	read_neighbours(g)
	g.authors[828114].edges[14607] = 4
	g.authors[14607].edges[828114] = 4
	return g

def experiment_phaze2(g, file_name):
	area = map(int, map(str.strip, open(file_name).readlines()))
	main_auth = area[0]
	area = area[1:]
	results = [["name", "simrank", "weighted simrank"]]
	for aid in area:
		print "computing author %d %s:"%(aid, g.authors[aid].name)
		ws = str(wsimrank(g, main_auth, aid, 3))
		print "wsimrank: " + ws
		s = str(simrank(g, main_auth, aid, 3))
		print "simrank: " + s
		results.append([g.authors[aid].name, s, ws])
	
	wr = csv.writer(open(file_name + ".csv", 'w'))
	wr.writerows(results)
