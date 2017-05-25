"""Genetic Python Module

This module provides a very basic framework that can be used to implement 
genetic algorithms.

Usage:
	To use this module, import the GeneticAlgorithm class and define a subclass
	with the genomeSize() and heuristic() functions declared as described 
	below.

	For more information, consult the README and examples.

"""

from abc import ABCMeta, abstractmethod
from random import uniform, randint
from operator import itemgetter
import sys

class Organism:
	""" A single organism in a population

	In general, this class shouldn't need to be overwritten.

	Attributes:
		geneCount (int): The number of genes that make up an orgnaism's genome.
		genes (float[]): The values of each gene in this organism's genome. Genes
		are float values from (0.0, 1.0).

	"""

	@classmethod
	def getChild(cls, parent1, parent2, mutationRate=0.1):
		"""Returns the offspring of two parent organisms

		Arguments:
			parent1 (Organism): An organism instance
			parent2 (Organism): An organism instance
			mutationRate (float, optional):
				A float (0.0, 1.0) that describes the probability of an
				arbitrary gene being randomly set rather than produced as a 
				function of the parents' genome.

		Returns:
			Organism: A new organism instance

		"""
		
		# These lines just make sure that we have two valid organisms
		assert parent1.geneCount == parent2.geneCount
		assert len(parent1.genes) == parent1.geneCount
		assert len(parent1.genes) == len(parent2.genes)

		child = Organism(parent1.geneCount)

		for g in range(0, parent1.geneCount):
			if uniform(0.0, 1.0) <= mutationRate:
				child.genes[g] = uniform(0.0, 1.0)
			else:
				# Crossover is performed by simply choosing the value of the
				# current gene from a random parent.
				if uniform(0.0, 1.0) <= 0.5:
					child.genes[g] = parent1.genes[g]
				else:
					child.genes[g] = parent2.genes[g]

		return child

	def __init__(self, geneCount):
		"""Organism constructor

		Initializes an organism with a set of random genes

		Arguments:
			geneCount (int): The number of genes in this organism's genome. >=0

		"""
		assert geneCount >= 0

		self.geneCount = geneCount
		self.genes = []

		for i in range (0, geneCount):
			self.genes.append (uniform(0.0, 1.0))

# An abstract genetic algorithm class. When implemented, a user should only
# override the abstract functions. The rest will be taken care of by this class.
class GeneticAlgorithm:
	"""The base class for genetic algorithms

	This class should not (and cannot) be instantiated. Instead, implement a
		subclass that implements the genomeSize() and heuristic() functions
		below.

	Attributes:
		generation (int): The current generation of this algorithm. >= 0
		geneCount (int): The number of genes in each organism's genome. >= 0
		popSize (int): The number of organisms in the population. >= 0
		population (Organism[]): The collection of organisms that are living.
		mutationRate (float): See Organism.getChild().
		eliteCount (int): The number of organisms that carry over to the next 
			generation. [0, popSize]
		parentCount (int): The number of parents that will be used to produce
			the next generation [0, popSize]
		childCount (int): The number of children produced for the next
			generation. popSize - eliteCount

	"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def genomeSize(self):
		""" Defines the number of genomes in an organisms's genome

		This function must be overrided.

		Returns:
			int: The number of genes in an organism's genome. >= 0

		"""

		pass

	@abstractmethod
	def heuristic(self, organism):
		""" Tests the fitness of a specific organism

		This function must be overrided. The genetic algorithms seeks to
			maximize this function

		Arguments:
			organism (Organism): The organism to be scored

		Returns:
			float: The fitness of the organism

		"""

		pass

	def __init__(self, popSize=100, mutationRate=0.1, elitism=0.0,
				 selectivity=0.5):
		"""Initializes a genetic algorithm with an initial population.

		This should be called in the constructor of subclasses.

		Arguments:
			popSize (int, optional): The number of individuals in a population.
				>= 0
			mutationRate (float, optional): See Organism.getChild().
			elitism (float, optional): The percentage of organisms that are
				preserved for the next generation. [0.0, 1.0]
			selectivity (float, optional): The percentage of organisms that are
				chosen as parents for the next generation. [0.0, 1.0]

		"""

		# Make sure that the preconditions are satisfied
		assert popSize >= 0
		assert mutationRate >= 0 and mutationRate <= 1
		assert elitism >= 0 and  elitism <= 1
		assert selectivity >= 0 and selectivity <= 1
		assert selectivity > elitism

		self.generation = 1
		self.geneCount = self.genomeSize()
		self.popSize = popSize
		self.population = self.__createPopulation (popSize)
		
		self.mutationRate = mutationRate
		self.eliteCount = int(round(self.popSize * elitism))
		self.parentCount = int(round(self.popSize * selectivity))
		self.childCount = self.popSize - self.eliteCount

	def __createPopulation(self, popSize):
		"""Initializes a random population
		
		This functions should not be used by subclasses.

		Arguments:
			popSize (int): The number of organisms in the population. >= 0

		Returns:
			Organism[]: A list of organisms
		"""

		assert popSize >= 0

		population = []
		
		for i in range(0, popSize):
			population.append (Organism(self.geneCount))

		return population

	def simulate(self, genCount=0, minScore=sys.maxint, verbose=False):
		"""Sets the genetic algorithm in motion
		
		Simulates the genetic algorithm until:
			1) genCount generations have elapsed
			2) An organism has a fitness >= minScore

		Arguments:
			genCount (int): The number of generations to simulate. >= 0
			minScore (float): The minimum score that qualifies as a solution.
			verbose (bool, optional): Whether or not to print the current
				generation and the best score of that generation for each 
				iteration

		Returns:
			Organism: The organism with the best score at the end of the 
				simulation

		"""

		assert genCount >= 0

		while (genCount > 0):
			genCount -= 1

			scoredPop = []

			for i in range(0, self.popSize):
				organism = self.population[i]
				scoredPop.append ((organism, self.heuristic(organism)))

			# Sort by descending score
			scoredPop = sorted(scoredPop, key=itemgetter(1), reverse=True)

			if verbose:
				print ("Generation: %d | Best score: %f" %
					   (self.generation, scoredPop[0][1]))

			# Check if this generation is satisfactory or if this is the last
			# iteration
			if scoredPop[0][1] >= minScore or genCount == 0:
				return scoredPop[0][0]

			
			# If not, produce the next one
			parents = [o[0] for o in scoredPop[0:self.parentCount]]
			self.population =  parents[0:self.eliteCount]

			for j in range(0, self.childCount):
				parent1 = parents[randint(0, self.parentCount - 1)]
				parent2 = parent1
				
				while parent2 == parent1:
					parent2 = parents[randint(0, self.parentCount - 1)]
				
				child = Organism.getChild(parent1, parent2, self.mutationRate)
				self.population.append (child)
			
			self.generation += 1
