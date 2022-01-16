import copy
import sys

from InformatiCupPy.com.informaticup.python.algorithms.AdvancedPassengerParallelizationAlgorithm import \
    AdvancedPassengerParallelizationAlgorithm
from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotParseInputException
from InformatiCupPy.com.informaticup.python.algorithms.SimpleDijkstraAlgorithm import SimpleDijkstraAlgorithm
from InformatiCupPy.com.informaticup.python.algorithms.SimplePassengerParallelizationAlgorithm import \
    SimplePassengerParallelizationAlgorithm
from InformatiCupPy.com.informaticup.python.algorithms.SimpleTrainParallelizationAlgorithm \
    import SimpleTrainParallelizationAlgorithm
from InformatiCupPy.com.informaticup.python.ioParsing.InputParser import InputParser
from InformatiCupPy.com.informaticup.python.ioParsing.OutputParser import OutputParser


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
    # input_str = open("InformatiCupPy/com/informaticup/input-output/input.txt", "r").read()

    # creates a list (length 4) of lists (length x), which contains several object parsed from the input file
    try:
        # input = InputParser("InformatiCupPy/com/informaticup/input-output/input.txt").parse_input()
        input = InputParser(sys.stdin.read()).parse_input()
        solvers = [
            SimpleDijkstraAlgorithm(copy.deepcopy(input)),
            SimplePassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=0),
            SimplePassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=0.3),
            SimplePassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=0.7),
            SimplePassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=1),
            AdvancedPassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=0),
            AdvancedPassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=0.3),
            AdvancedPassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=0.7),
            AdvancedPassengerParallelizationAlgorithm(copy.deepcopy(input), capacity_speed_ratio=1),

            SimpleTrainParallelizationAlgorithm(copy.deepcopy(input), set_wildcards=0.0, parallelization_factor=0.0),
            SimpleTrainParallelizationAlgorithm(copy.deepcopy(input), set_wildcards=0.0),
            SimpleTrainParallelizationAlgorithm(copy.deepcopy(input), parallelization_factor=0.2),
            SimpleTrainParallelizationAlgorithm(copy.deepcopy(input))
        ]
        # OutputParser.parse_output_files(solvers, input)
        OutputParser.parse_output_files_to_stdout(solvers, input)
    except CannotParseInputException as ex:
        ex.print_message()


main()
