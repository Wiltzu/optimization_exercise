import itertools

class City(object):
	"""docstring for City"""
	def __init__(self, number, x, y):
		super(City, self).__init__()
		self.number = number
		self.x = x
		self.y = y

	def __repr__(self):
		return 'City[number="%s", x="%s", y="%s"]' % (self.number, self.x, self.y)


def get_distance_matrix(data):
	distance_matrix = []
	cities = []
	
	for line in data:
		if line[0].isdigit():
			number, x, y = line.strip().split(' ')
			cities.append(City(number, x, y))



	print(cities[0])
	return distance_matrix

def main():
	f = open('fi10639.tsp')
	distance_mat = get_distance_matrix(f.readlines())
	

if __name__ == '__main__':
	main()