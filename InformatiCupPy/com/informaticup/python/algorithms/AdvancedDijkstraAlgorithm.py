from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver


class EasyDijkstraAlgorithm(ISolver):

    # TODO: improve the easy version of this algorithm with the following ideas:
    #  - passenger priority based on target time, group size
    #  - take more passengers in one train
    #  - improve calculation time using a database for already calculated shortest paths

    def solve(self, input: list) -> int:
        pass

    def get_name(self):
        """
        name of the algorithm (used to name the output file)
        :return: name of the algorithm
        """
        return "advanced-dijkstra-algorithm"
