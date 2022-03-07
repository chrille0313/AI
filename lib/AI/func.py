from numpy import exp


def sigmoid(x):
	return 1/(1 + exp(-x))


def relu(x):
	return x * (x > 0)


def linear(x):
	return x
