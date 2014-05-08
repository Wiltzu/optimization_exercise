import itertools
import numpy as np
import logging
import sys
import random

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
	return distance

def random_cities(n):
	return set(City(c, random.randrange(10, 800), random.randrange(10, 500)) for c in range(n))

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
	
	if len(cities) <= 10:
		optimal_tour = bruteforce_solve(cities)
		print(total_distance(optimal_tour))


if __name__ == '__main__':
	main()