from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver


class SimpleAlgorithmSolver(ISolver):

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lanes = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]
    """ Example solver-class. """
    def solve(self, input):
        # algorithm solves problem (input) here
        result = ""
        return result

    def get_name(self):
        return "simple-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]