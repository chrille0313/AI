from abc import abstractmethod


class GeneticAgent:
	def __int__(self):
		pass

	@property
	@abstractmethod
	def fitness(self):
		raise Exception("Fitness property must be defined!")


