from InformatiCupPy.com.informaticup.python.algorithms.SimpleAlgorithmSolver import SimpleAlgorithmSolver
from InformatiCupPy.com.informaticup.python.ioParsing.InputParser import InputParser
from InformatiCupPy.com.informaticup.python.ioParsing.OutputParser import OutputParser


def main():
    input = InputParser("../input-output/input.txt").parse_input()
    for i in input:
        for j in i:
            print(j.to_string())
    print(input)

    solvers = [SimpleAlgorithmSolver()]
    OutputParser.parse_output_files(solvers, input)


main()
