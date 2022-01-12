import sys

from InformatiCupPy.com.informaticup.python.objects.Line import Line
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.objects.Station import Station
from InformatiCupPy.com.informaticup.python.objects.Train import Train
import re
from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotParseInputException


class InputParser:

    def __init__(self, input_path):
        self.input = open(input_path).read().split("\n")

    """Parses stations form input and creates station objects with the input parameters and returns them as list."""

    def parse_stations(self):
        stations = []
        station = False

        for i, line in enumerate(self.input):
            if station:
                splittedLine = line.split(" ")

                if self.check_station_string(splittedLine):
                    stations.append(Station(splittedLine[0], splittedLine[1]))
                elif self.check_passenger_string(splittedLine) or self.check_line_string(splittedLine) or self.check_train_string(splittedLine) or line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]" or line == "":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Stations]":
                station = True

        return stations

    """Parses lanes form input and creates lane objects with the input parameters and returns them as list."""

    def parse_lines(self):
        lines = []
        line_bool = False

        for i, line in enumerate(self.input):
            if line_bool:
                splittedLine = line.split(" ")

                if self.check_line_string(splittedLine):
                    connected_stations = [splittedLine[1], splittedLine[2]]
                    lines.append(Line(splittedLine[0], connected_stations, splittedLine[3], splittedLine[4]))
                elif self.check_passenger_string(splittedLine) or self.check_station_string(splittedLine) or self.check_train_string(splittedLine) or line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]" or line == "":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Lines]":
                line_bool = True

        return lines

    """Parses trains form input and creates train objects with the input parameters and returns them as list."""

    def parse_trains(self):
        trains = []
        train = False

        for i, line in enumerate(self.input):
            if train:
                splittedLine = line.split(" ")

                if self.check_train_string(splittedLine):
                     trains.append(Train(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3]))
                elif self.check_passenger_string(splittedLine) or self.check_station_string(
                        splittedLine) or self.check_line_string(splittedLine) or line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]" or line == "":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Trains]":
                train = True
        return trains

    """Parses passengers form input and creates passenger objects with the input parameters and returns them as list."""

    def parse_passengers(self):
        passengers = []
        passenger = False

        for i, line in enumerate(self.input):
            if passenger:
                splittedLine = line.split(" ")

                if self.check_passenger_string(splittedLine):
                    passengers.append(Passenger(splittedLine[0],
                                                splittedLine[1],
                                                splittedLine[2],
                                                splittedLine[3],
                                                splittedLine[4]))
                elif self.check_train_string(splittedLine) or self.check_station_string(
                        splittedLine) or self.check_line_string(splittedLine) or line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]" or line == "":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Passengers]":
                passenger = True

        return passengers

    """Checks wether a input line split into an string array is a valid station string"""

    def check_station_string(self, stringList):
        if stringList.__len__() == 2:
            if stringList[0].startswith("S"):
                try:
                    if str(stringList[0]).__len__() == 2:
                        idNumber = int(str(stringList[0])[1])
                    else:
                        idNumber = int(str(stringList[0]+" ")[1:str(stringList[0]).__len__()])

                    cap = int(stringList[1])

                    return True
                except:
                    return False
            else:
                return False
        else:
            return False

    """Checks wether a input line split into an string array is a valid line string"""

    def check_line_string(self, stringList):
        if stringList.__len__() == 5:
            if stringList[0].startswith("L") and stringList[1].startswith("S") and stringList[2].startswith("S"):
                try:
                    if str(stringList[0]).__len__() == 2:
                        idNumber = int(str(stringList[0])[1])
                    else:
                        idNumber = int(str(stringList[0]+" ")[1:str(stringList[0]).__len__()])

                    if str(stringList[1]).__len__() == 2:
                        startStation = int(str(stringList[1])[1])
                    else:
                        startStation = int(str(stringList[1]+" ")[1:str(stringList[1]).__len__()])

                    if str(stringList[2]).__len__() == 2:
                        endStation = int(str(stringList[2])[1])
                    else:
                        endStation = int(str(stringList[2]+" ")[1:str(stringList[2]).__len__()])

                    length = float(stringList[3])
                    cap = int(stringList[4])

                    return True
                except:
                    return False
            else:
                return False
        else:
            return False

    """Checks wether a input line split into an string array is a valid train string"""

    def check_train_string(self, stringList):
        if stringList.__len__() == 4:
            if stringList[0].startswith("T"):
                try:
                    if str(stringList[0]).__len__() == 2:
                        idNumber = int(str(stringList[0])[1])
                    else:
                        idNumber = int(str(stringList[0]+" ")[1:str(stringList[0]).__len__()])

                    speed = float(stringList[2])
                    cap = int(stringList[3])

                    if stringList[1] == "*":
                        return True
                    elif stringList[1].startswith("S"):
                        if str(stringList[1]).__len__() == 2:
                            startStation = int(str(stringList[1])[1])
                        else:
                            startStation = int(str(stringList[1]+" ")[1:str(stringList[1]).__len__()])
                        return True
                    else:
                        return False
                except:
                    return False
            else:
                return False
        else:
            return False

    """Checks wether a input line split into an string array is a valid passengers string"""

    def check_passenger_string(self, stringList):
        if stringList.__len__() == 5:
            if stringList[0].startswith("P") and stringList[1].startswith("S") and stringList[2].startswith("S"):
                try:
                    if str(stringList[0]).__len__() == 2:
                        idNumber = int(str(stringList[0])[1])
                    else:
                        idNumber = int(str(stringList[0]+" ")[1:str(stringList[0]).__len__()])

                    if str(stringList[1]).__len__() == 2:
                        startStation = int(str(stringList[1])[1])
                    else:
                        startStation = int(str(stringList[1]+" ")[1:str(stringList[1]).__len__()])

                    if str(stringList[2]).__len__() == 2:
                        endStation = int(str(stringList[2])[1])
                    else:
                        endStation = int(str(stringList[2]+" ")[1:str(stringList[2]).__len__()])


                    groupSize = int(stringList[3])
                    time = int(stringList[4])

                    return True
                except:
                    return False
            else:
                return False
        else:
            return False



    """Parses stations, lanes, trains and passengers from input and returns a list of those objects as list."""

    def parse_input(self):
        #TODO Exception handling in output_parser
            objects = [self.parse_stations(), self.parse_lines(), self.parse_trains(), self.parse_passengers()]
            return objects



