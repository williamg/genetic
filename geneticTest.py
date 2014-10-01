from genetic import GeneticAlgorithm
import sys

class GeneticAlgoTest(GeneticAlgorithm):
	def __init__(self):
		super(GeneticAlgoTest, self).__init__()

	def genomeSize(self):
		return 8

	def heuristic(self, organism):
		assert organism.geneCount == 8
		assert len(organism.genes) == 8

		binary = []
		for g in range(0, 8):
			binary.append(round(organism.genes[g]))

		x = self.binToInt (binary)

		# Max = 100
		return  -pow(x-100, 4) + pow(x-100, 2) + x - 100

	def binToInt (self, binary):
		val = 0
		for b in range (0, len(binary)):
			val = (2 * val) + binary[b]

		return val

if __name__ == "__main__":
	alg = GeneticAlgoTest()
	alg.simulate (genCount=10000, verbose=True)

	bestVal = None
	bestScore = -sys.maxint - 1

	for i in range (0, alg.popSize):
		if alg.heuristic(alg.population[i]) > bestScore:
			binary = []
			organism = alg.population[i]
			for g in range(0, 8):
				binary.append(round(organism.genes[g]))

			bestVal = alg.binToInt (binary)

	print ("Best val: ", bestVal)



