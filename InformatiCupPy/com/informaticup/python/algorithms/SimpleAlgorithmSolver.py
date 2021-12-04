from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver


class SimpleAlgorithmSolver(ISolver):
    """ Example solver-class. """
    def solve(self, input):
        # algorithm solves problem (input) here
        result = "result"
        return result

    def get_name(self):
        return "simple-algorithm"