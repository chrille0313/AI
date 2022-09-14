import numpy as np
from typing import Union


def sigmoid(x: Union[int, float]) -> float:
	return 1/(1 + np.exp(-x))


def relu(x: Union[int, float]) -> Union[int, float]:
	return np.maximum(0, x)


def linear(x: Union[int, float]) -> Union[int, float]:
	return x


def tanh(x: Union[int, float]) -> float:
	return np.tanh(x)
