import sys

from InformatiCupPy.com.informaticup.python.algorithms.EasyDijkstraAlgorithm import EasyDijkstraAlgorithm
from InformatiCupPy.com.informaticup.python.algorithms.SimpleAlgorithmSolver import SimpleAlgorithmSolver
from InformatiCupPy.com.informaticup.python.ioParsing.InputParser import InputParser
from InformatiCupPy.com.informaticup.python.ioParsing.OutputParser import OutputParser


def __main__():
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

    input_str = open("InformatiCupPy/com/informaticup/input-output/input.txt", "r").read()

    # input = InputParser(input_str).parse_input()
    # solvers = [SimpleAlgorithmSolver(), EasyDijkstraAlgorithm()]
    # OutputParser.parse_output_files(solvers, input)
    # print(open("InformatiCupPy/com/informaticup/input-output/output.txt").read())

    input_file = InputParser(sys.stdin.read()).parse_input()
    solvers = [SimpleAlgorithmSolver(), EasyDijkstraAlgorithm()]
    OutputParser.parse_output_files_to_stdout(solvers, input_file)





__main__()