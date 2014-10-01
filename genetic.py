# Genetic Algorithm python module
# Written by William Ganucheau 2014
from abc import ABCMeta, abstractmethod
from random import uniform, randint
from operator import itemgetter
import sys

# Basic organism class
class Organism:
	@classmethod
	def getChild(cls, parent1, parent2, mutationRate=0.1):
		assert parent1.geneCount == parent2.geneCount
		assert len(parent1.genes) == parent1.geneCount
		assert len(parent1.genes) == len(parent2.genes)

		child = Organism(parent1.geneCount)

		for g in range(0, parent1.geneCount):
			if uniform(0.0, 1.0) <= mutationRate:
				child.genes[g] = uniform(0.0, 1.0)
			else:
				if uniform(0.0, 1.0) <= 0.5:
					child.genes[g] = parent1.genes[g]
				else:
					child.genes[g] = parent2.genes[g]

		return child

	def __init__(self, geneCount):
		assert geneCount >= 0

		self.geneCount = geneCount
		self.genes = []

		for i in range (0, geneCount):
			self.genes.append (uniform(0.0, 1.0))

# An abstract genetic algorithm class. When implemented, a user should only
# override the abstract functions. The rest will be taken care of by this class.
class GeneticAlgorithm:
	__metaclass__ = ABCMeta

	# This function defines the size (number of variables) in the genome. It 
	# should return an integer.
	@abstractmethod
	def genomeSize(self):
		pass

	# This function should take in an Organism object and evaluate it to return
	# some score. The genetic algorithm tries to maximimize this function.
	@abstractmethod
	def heuristic(self, organism):
		pass



	def __init__(self, popSize=100, mutationRate=0.1, elitism=0.0,
				 selectivity=0.5):
		assert popSize >= 0
		assert mutationRate >= 0
		assert elitism >= 0
		assert selectivity >= 0
		assert selectivity > elitism

		self.generation = 1
		self.geneCount = self.genomeSize()
		self.popSize = popSize
		self.population = self.__createPopulation (popSize)

		#Config parameters
		self.mutationRate = mutationRate
		self.eliteCount = int(round(self.popSize * elitism))
		self.parentCount = int(round(self.popSize * selectivity))
		self.childCount = self.popSize - self.eliteCount

	def __createPopulation(self, popSize):
		assert popSize >= 0

		population = []
		
		for i in range(0, popSize):
			population.append (Organism(self.geneCount))

		return population

	def simulate(self, genCount=0, minScore=sys.maxint, verbose=False):
		assert genCount >= 0

		while (genCount > 0):
			genCount -= 1
			self.generation += 1
			scoredPop = []

			for i in range(0, self.popSize):
				organism = self.population[i]
				scoredPop.append ((organism, self.heuristic(organism)))

			# Sort by descending score
			scoredPop = sorted(scoredPop, key=itemgetter(1), reverse=True)

			if verbose:
				print ("Generation: ", self.generation)
				print ("Best score: ",  scoredPop[0][1])

			# Check if this generation is satisfactory
			if scoredPop[0][1] >= minScore:
				return scoredPop
			
			# If not, produce the next one
			parents = [o[0] for o in scoredPop[0:self.parentCount]]
			elites = parents[0:self.eliteCount]
			self.population = elites

			for j in range(0, self.childCount):
				parent1 = parents[randint(0, self.parentCount - 1)]
				parent2 = parent1
				
				while parent2 == parent1:
					parent2 = parents[randint(0, self.parentCount - 1)]
				
				child = Organism.getChild(parent1, parent1, self.mutationRate)

				self.population.append (child)
	
