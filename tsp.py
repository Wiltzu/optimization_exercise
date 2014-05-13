import itertools
import numpy as np
import logging
import sys
import random
import time
import matplotlib
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(' tsp ')

random.seed('seed')

### DOMAIN CLASSES ###

class Point(complex): pass

class City(object):
	"""docstring for City"""
	def __init__(self, number, x, y):
		super(City, self).__init__()
		self.number = number
		self.x = x
		self.y = y
		self.point = Point(x, y)

	def __repr__(self):
		return 'City[number="%s", x="%s", y="%s"]' % (self.number, self.x, self.y)

### HELPER FUNTIONS ###

def get_cities(data):
	cities = []
	
	for line in data:
		if line[0].isdigit():
			number, x, y = line.strip().split(' ')
			cities.append(City(int(number), float(x), float(y)))

	return cities

	
def all_tours(cities):
	"""(n-1)! different permutations"""
	start = first(cities)
	return [[start] + list(tour)
	    for tour in itertools.permutations(cities - {start})]

def first(collection):
    for x in collection: return x

def total_distance(tour):
	return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def distance(cityA, cityB):
	if cityA == cityB:
		return 0
	else:
		return abs(cityA.point - cityB.point)


def random_cities(n):
	return set(City(c, random.randrange(10, 800), random.randrange(10, 500)) for c in range(n))

def ascending_order(edges):
	edges.sort(key=lambda (A, B): distance(A, B))
	return edges

### TOUR PLOTTING ###

def plot_tour(tour):
    """Plot the resulting tour."""
    # Plot the tour as blue lines between blue circles, and the starting city as a red square.
    plotline(list(tour) + [tour[0]])
    plotline([tour[0]], 'rs')
    plt.show()
    
def plotline(cities, style='bo-'):
    "Plot a list of points (complex numbers) in the 2-D plane."
    X, Y = XY(cities)
    plt.plot(X, Y, style)
    
def XY(cities):
    "Given a list of points, return two lists: X coordinates, and Y coordinates."
    return [p.x for p in cities], [p.y for p in cities]

### GREEDY SOLVERS ###

def bruteforce_solve(cities):
	tours = all_tours(cities)
	return min(tours, key=total_distance)

def nearest_merger(cities):
	N = len(cities)
	
	edges = ascending_order([(A, B) for A in cities for B in cities if abs(A.point) < abs(B.point)])
	# partial tours containing city C
	partial_tours = {C: [C] for C in cities}
	for (A, B) in edges:
		join_partial_tours(partial_tours, A, B)
		if len(partial_tours[A]) == len(cities):
			return partial_tours[A]

def join_partial_tours(partial_tours, A, B):
	partial_tourA = partial_tours[A]
	partial_tourB = partial_tours[B]
	ptA_ending_edge = (partial_tourA[0], partial_tourA[-1])
	ptB_ending_edge = (partial_tourB[0], partial_tourB[-1])

	# partial tours are not connected AND
	# A and B are in the end or start of partial tour because the order must remain
	if partial_tourA is not partial_tourB and A in ptA_ending_edge and B in ptB_ending_edge:
		#arrange that partial tour A ends with city A and partial tour B ends with B
		if partial_tourA[0] == A: 
			partial_tourA.reverse()
		if partial_tourB[-1] == B:
			partial_tourB.reverse()
		partial_tourA += partial_tourB
		for city in partial_tourB:
			partial_tours[city] = partial_tourA
		return partial_tourB

### Local Search ###

def two_opt(tour, max_iterations=100, min_improvement_percent=0.0005):	
	improved = True
	iteration = 0
	while improved and iteration <= max_iterations:
		print('iteration: %s' % iteration)
		improved = improve(tour, min_improvement_percent)
		iteration = iteration + 1
	return tour

def improve(tour, min_improvement_percent):
	total_distance_before = total_distance(tour)
	minimum_improvement =  total_distance_before * min_improvement_percent
	edges = [(i, i+1) for i in range(len(tour)-1)]
	edges.append((len(tour)-1, 0))
	for a, b in edges:
		for c, d in edges:
			if a not in [c, d] and b not in [c, d]:
				tour[b], tour[c] = tour[c], tour[b]
				total_distance_after = total_distance(tour)
				improvement = total_distance_before - total_distance_after
				if improvement < minimum_improvement:
					tour[b], tour[c] = tour[c], tour[b]
				else:
					print('tour improved by %s' % (total_distance_before - total_distance_after))
					return True
		#drop 1st edge because all its pairs have been explored
		edges.pop(0)


	return False

### MAIN METHOD ###

def main():
	cities, tour = None, None
	if len(sys.argv) > 1:
		if sys.argv[1] == 'random':
			if sys.argv[2]:
				cities = random_cities(int(sys.argv[2]))
			else:
				_LOGGER.error(" If random is used size of data must be given also like 'random 10'")
				sys.exit(-1)
		else:
			filename = sys.argv[1]
			tour_filename = filename.replace(".tsp", ".tour")
			try:
				tour_file = open(tour_filename)
				_LOGGER.info(" importing precalculated tour from file.")
				tour = get_cities(tour_file.readlines())
			except IOError, e:
				tsp_file = open(filename)
				cities = set(get_cities(tsp_file.readlines()))
	else:
		_LOGGER.error(" Give TSPLIB data 'filename' as parameter OR 'random' with its data size.")
		sys.exit(-1)
	
	number_of_cities = len(cities) if cities else len(tour)
	print("%s city tour" % number_of_cities)
	
	if tour == None:
		start_time = time.clock()
		if number_of_cities <= 10:
			_LOGGER.info(" There are 10 or less cities, so let's use brute-force algorithm.")
			tour = bruteforce_solve(cities)
		else:
			_LOGGER.info(" There are more than 10 cities, so let's use nearest merger algorithm.")
			tour = nearest_merger(cities)
		end_time = time.clock()

		distance_before =total_distance(tour)
		print("Construction algorithm: total distance = {:.2f}; time = {:.3f} secs".format(
			distance_before, end_time-start_time))
	else:
		distance_before = total_distance(tour)
		print("Construction algorithm: total distance = {:.2f}".format(distance_before))

	if tour_file == None:
		save_tour_to_file(tour, tour_filename)

	plot_tour(tour)

	min_improvement_percent = 0.00001
	max_iterations = 100
	print("Improving tour with local search with \nminimum improvement percent {} and maximum number of iterations {}...".format(
		min_improvement_percent, max_iterations))
	start_time = time.clock()
	_2opt = two_opt(tour, max_iterations, min_improvement_percent)
	end_time = time.clock()
	
	print("2-Opt took {:.3f} secs".format(end_time-start_time))
	print("Before 2-opt: total distance = {:.2f} \nAfter  2-Opt: total distance = {:.2f}".format(
		distance_before, total_distance(_2opt)))
	plot_tour(_2opt)


def save_tour_to_file(tour, tour_filename):
	_LOGGER.info(" Writing tour to file.")
	formatted_tour = ['%s %s %s' % (city.number, city.x, city.y) for city in tour]
	tour_data = "\n".join(formatted_tour)  
	open(tour_filename, "w+").write(tour_data)

if __name__ == '__main__':
	main()