from snake.base.pos import Pos
from snake.base import Direc
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver

class NeuralSolver(BaseSolver):

	def __init__(self, sanek):
		super().__init__(snake)
		self.__path_solver = PathSolver(snake)

	def next_direc(self):
		# input?

		return direc
