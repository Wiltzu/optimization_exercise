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

_DISTANCE_MATRIX = []

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

	return set(cities)

	
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

	distance = _DISTANCE_MATRIX[cityA.number][cityB.number]
	if distance == 0:
		distance = abs(cityA.point - cityB.point)
		_DISTANCE_MATRIX[cityA.number][cityB.number] = distance
		# distance is symmetric 
		_DISTANCE_MATRIX[cityB.number][cityA.number] = distance
	return distance

def random_cities(n):
	return set(City(c, random.randrange(10, 800), random.randrange(10, 500)) for c in range(n))

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

### SOLVERS ###

def bruteforce_solve(cities):
	tours = all_tours(cities)
	return min(tours, key=total_distance)

### MAIN METHOD ###

def main():
	if len(sys.argv) > 1:
		if sys.argv[1] == 'random':
			if sys.argv[2]:
				cities = random_cities(int(sys.argv[2]))
			else:
				_LOGGER.error(" If random is used size of data must be given also like 'random 10'")
				sys.exit(-1)
		else:
			f = open(sys.argv[1])
			cities = get_cities(f.readlines())
	else:
		_LOGGER.error(" Give TSPLIB data 'filename' as parameter OR 'random' with its data size.")
		sys.exit(-1)

	for i in range(len(cities)):
		_DISTANCE_MATRIX.append([0]*len(cities))
	
	start_time = time.clock()
	tour = None
	if len(cities) <= 10:
		tour = bruteforce_solve(cities)
	else:
		_LOGGER.info(" There are more than 10 cities.")
	end_time = time.clock()

	if tour:
		print("{} city lenght tour; total distance = {:.2f}; time = {:.3f} secs".format(
			len(tour), total_distance(tour), end_time-start_time))
		plot_tour(tour)
	else:
		_LOGGER.info(" Tour was not calculated.")


if __name__ == '__main__':
	main()