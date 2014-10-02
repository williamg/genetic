Genetic
===

Genetic is a python library for easily implementing genetic algorithms

Usage
---
To use genetic, first import the `GeneticAlgorithm` class and create a subclass:

    from genetic import GeneticAlgorithm
    
    class GenAlgSubclass (GeneticAlgorithm):
        def __init__(self):
            super(GenAlgSubclass, self).__init__()
            

Your subclass needs to implement two functions:
    
	def genomeSize(self):
		""" Defines the number of genomes in an organisms's genome

		This function must be overrided.

		Returns:
			int: The number of genes in an organism's genome. >= 0

		"""

		# Your implemenetation here...

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

		# Your implementation here
		

To compute the fitness of the organism, you can use `organism.genes` which is a list of floats [0, 1] that contains the value of each gene in the organism's genome.

Once your subclass has been implemented, you can run the algorithm using the `simulate()` method:

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
		

Simply call this function from your subclass:

    myAlg = GenAlgSubclass()
    winningOrganism = myAlg.simulate()
    
---
Developed by William Ganucheau. Released under the MIT License.

