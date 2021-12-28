from InformatiCupPy.com.informaticup.python.algorithms.EasyDijkstraAlgorithm import EasyDijkstraAlgorithm
from InformatiCupPy.com.informaticup.python.algorithms.SimpleAlgorithmSolver import SimpleAlgorithmSolver
from InformatiCupPy.com.informaticup.python.ioParsing.InputParser import InputParser
from InformatiCupPy.com.informaticup.python.ioParsing.OutputParser import OutputParser
import copy


def main():
    """
    List order + each variables:
        1 Stations
            id, capacity
        2 Lanes
            id, connected_stations, length, capacity
        3 Trains
            id, capacity, speed, position
        4 Passengers
            id, initial_station, target_station, group_size, target_time
    """

    # creates a list (length 4) of lists (length x), which contains several object parsed from the input file
    input = InputParser("../input-output/input.txt").parse_input()
    solvers = [SimpleAlgorithmSolver(copy.deepcopy(input)), EasyDijkstraAlgorithm(copy.deepcopy(input))]
    OutputParser.parse_output_files(solvers, input)


main()
