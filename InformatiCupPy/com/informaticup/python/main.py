
from com.informaticup.python.ioParsing.InputParser import InputParser

def main():
    input = InputParser("com/informaticup/input-output/input.txt").parse_input()
    for i in input:
        for j in i:
            print(j.to_string())

main()


