from genetic import GeneticAlgorithm

# This is a simple example that uses a genetic algorithm to maximize a function
class Maximizer(GeneticAlgorithm):
	def __init__(self):
		super(Maximizer, self).__init__()

	# Organisms will represent 8-bit integers
	def genomeSize(self):
		return 8

	# Heuristic function will simply be the value of the function at the x
	# value represented by the organism
	def heuristic(self, organism):
		assert organism.geneCount == 8
		assert len(organism.genes) == 8

		binary = []
		for g in range(0, 8):
			binary.append(round(organism.genes[g]))

		x = self.binToInt (binary)
		return self.functionToMaximize (x)

	# Convert a list of binary bits to an integer
	def binToInt (self, binary):
		val = 0
		for b in range (0, len(binary)):
			val = (2 * val) + binary[b]

		return val

	# The function we want to maximize
	def functionToMaximize(self, x):
		# Max = 100
		return -pow(x-100, 4) + pow(x-100, 2) + x - 100

if __name__ == "__main__":
	findMax = Maximizer()
	organism = findMax.simulate (genCount=1000, verbose=False)

	binary = []
	for g in range(0, 8):
		binary.append(round(organism.genes[g]))

	bestVal = findMax.binToInt (binary)

	print ("Approximate maximum: %d" % bestVal)

