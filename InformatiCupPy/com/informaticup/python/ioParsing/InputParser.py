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
        stationRegexpression = re.compile("\A(?P<id>[a-zA-Z0-9_]+) (?P<kapazitaet>[\d]+)[\s]*\z")

        for i, line in enumerate(self.input):
            if line == "":
                station = False
            if station:
                station_str = line.split(" ")

                if self.check_station_string(station_str):
                    stations.append(Station(station_str[0], station_str[1]))
                elif self.check_passenger_string(station_str) or self.check_line_string(station_str) or self.check_train_string(station_str) or station_str[1][0] == "#" or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
              #  stations.append(Station(station_str[0], station_str[1]))
              #  if stationRegexpression.match(line):
            if line == "[Stations]":
                station = True

        return stations

    """Parses lanes form input and creates lane objects with the input parameters and returns them as list."""

    def parse_lanes(self):
        lanes = []
        lane = False

        for i, line in enumerate(self.input):
            if line == "":
                lane = False
            if lane:
                lane_str = line.split(" ")
                connected_stations = [lane_str[1], lane_str[2]]
                lanes.append(Line(lane_str[0], connected_stations, lane_str[3], lane_str[4]))
            if line == "[Lines]":
                lane = True

        return lanes

    """Parses trains form input and creates train objects with the input parameters and returns them as list."""

    def parse_trains(self):
        trains = []
        train = False

        for i, line in enumerate(self.input):
            if line == "":
                train = False
            if train:
                train_str = line.split(" ")
                trains.append(Train(train_str[0], train_str[1], train_str[2], train_str[3]))
            if line == "[Trains]":
                train = True
        return trains

    """Parses passengers form input and creates passenger objects with the input parameters and returns them as list."""

    def parse_passengers(self):
        passengers = []
        passenger = False

        for i, line in enumerate(self.input):
            if line == "":
                passenger = False
            if passenger:
                passenger_str = line.split(" ")
                passengers.append(Passenger(passenger_str[0],
                                            passenger_str[1],
                                            passenger_str[2],
                                            passenger_str[3],
                                            passenger_str[4]))

            if line == "[Passengers]":
                passenger = True

        return passengers

    """Checks wether a input line split into an string array is a valid station string"""

    def check_station_string(self, stringList):
        if stringList.__len__() == 2:
            if stringList[0].startswith("S"):
                try:
                    idNumber = int(stringList[0][1, stringList.index(" ")])
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
                    idNumber = int(stringList[0][1, stringList.index(" ")])
                    startStation = int(stringList[1][1, stringList.index(" ")])
                    endStation = int(stringList[2][1, stringList.index(" ")])
                    length = int(stringList[3])
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
                    idNumber = int(stringList[0][1, stringList.index(" ")])
                    speed = int(stringList[2])
                    cap = int(stringList[3])

                    if stringList[1] == "*":
                        return True
                    elif stringList[1].startswith("S"):
                        startStation = int(stringList[1][1, stringList.index(" ")])
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
                    idNumber = int(stringList[0][1, stringList.index(" ")])
                    startStation = int(stringList[1][1, stringList.index(" ")])
                    endStation = int(stringList[2][1, stringList.index(" ")])
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


        objects = [self.parse_stations(), self.parse_lanes(), self.parse_trains(), self.parse_passengers()]

        return objects
