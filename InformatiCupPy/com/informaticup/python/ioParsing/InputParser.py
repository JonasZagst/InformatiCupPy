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
        stations_original = []
        stations = []
        counter = 0
        station = False

        for i, line in enumerate(self.input):
            if line.__contains__("[Lines]") or line.__contains__("[Trains]") or line.__contains__("[Passengers]"):
                station = False
            if station:
                splittedLine = line.split(" ")

                if self.check_station_string(splittedLine):
                    stations_original.append(Station(splittedLine[0], splittedLine[1]))
                elif line.startswith("#") or line == "" or line == "[Trains]" or line == "[Lines]" or line == "[Stations]" or line == "[Passengers]" or self.check_line_string(splittedLine) or self.check_train_string(splittedLine) or self.check_passenger_string(splittedLine):
                    continue
                else:
                    print(line)
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Stations]":
                station = True

        # setting the actualy used IDs
        for s in stations_original:
            counter = counter + 1
            s.set_internal_id("S"+str(counter))
            stations.append(s)

        return stations

    """Parses lanes form input and creates lane objects with the input parameters and returns them as list."""

    def parse_lines(self, station_array):
        lines_original = []
        lines = []
        counter = 0
        line_bool = False

        for i, line in enumerate(self.input):
            if line.__contains__("[Stations]") or line.__contains__("[Trains]") or line.__contains__("[Passengers]"):
                line_bool = False
            if line_bool:
                splittedLine = line.split(" ")

                if self.check_line_string(splittedLine):
                    connected_stations = [splittedLine[1], splittedLine[2]]
                    lines_original.append(Line(splittedLine[0], connected_stations, splittedLine[3], splittedLine[4]))
                elif self.check_passenger_string(splittedLine) or self.check_station_string(splittedLine) or self.check_train_string(splittedLine) or line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]" or line == "":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Lines]":
                line_bool = True

        # setting the actualy used IDs
        for l in lines_original:
            counter = counter + 1
            l.set_internal_id("L"+str(counter))
            original_stations = l.get_original_connected_stations()
            internal_stations = []
            first_station = ""
            second_station = ""

            for st in station_array:

                if str(st.get_original_id()).__contains__(original_stations[0]):
                    first_station = st.get_internal_id()
                elif str(st.get_original_id()).__contains__(original_stations[1]):
                    second_station = st.get_internal_id()

            internal_stations.append(first_station)
            internal_stations.append(second_station)

            l.set_internal_connected_stations(internal_stations)
            lines.append(l)

        return lines

    """Parses trains form input and creates train objects with the input parameters and returns them as list."""

    def parse_trains(self, station_array):
        trains_original = []
        trains = []
        train = False
        counter = 0

        for i, line in enumerate(self.input):
            if line.__contains__("[Stations]") or line.__contains__("[Lines]") or line.__contains__("[Passengers]"):
                train = False
            if train:
                splittedLine = line.split(" ")

                if self.check_train_string(splittedLine):
                     trains_original.append(Train(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3]))
                elif self.check_passenger_string(splittedLine) or self.check_station_string(
                        splittedLine) or self.check_line_string(splittedLine) or line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or line == "[Passengers]" or line == "":
                    continue
                else:
                    raise CannotParseInputException("Cannot read Input, unknown line in file")
            if line == "[Trains]":
                train = True

        # setting the actualy used IDs
        for t in trains_original:
            counter = counter + 1
            t.set_internal_id("T"+str(counter))

            if t.get_original_position() == "*":
                t.set_internal_position("*")
                trains.append(t)
                continue
            else:
                for st in station_array:

                    if  str(st.get_original_id()).__contains__(str(t.get_original_position())):
                        t.set_internal_position(st.to_string().split(" ")[0])

            trains.append(t)

        return trains

    """Parses passengers form input and creates passenger objects with the input parameters and returns them as list."""

    def parse_passengers(self, station_array):
        passengers_original = []
        passengers = []
        counter = 0
        passenger = False

        for i, line in enumerate(self.input):
            if line.__contains__("[Stations]") or line.__contains__("[Trains]") or line.__contains__("[Lines]"):
                passenger = False
            if passenger:
                splittedLine = line.split(" ")

                if self.check_passenger_string(splittedLine):
                    passengers_original.append(Passenger(splittedLine[0],
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

        # setting the actualy used IDs
        for p in passengers_original:
            counter = counter + 1
            p.set_internal_id("P" + str(counter))

            for st in station_array:
                if  str(st.get_original_id()).__contains__(str(p.get_original_initial_station())):
                    p.set_initial_station(st.to_string().split(" ")[0])
                elif  str(st.get_original_id()).__contains__(str(p.get_original_target_station())):
                    p.set_target_station(st.to_string().split(" ")[0])

            passengers.append(p)

        return passengers

    """Checks wether a input line split into an string array is a valid station string"""

    def check_station_string(self, stringList):
        if stringList.__len__() == 2:
                try:
                    cap = int(stringList[1])

                    return True
                except:
                    return False
        else:
            return False

    """Checks wether a input line split into an string array is a valid line string"""

    def check_line_string(self, stringList):
        if stringList.__len__() == 5:
                try:

                    length = float(stringList[3])
                    cap = int(stringList[4])

                    return True
                except:
                    return False
        else:
            return False

    """Checks wether a input line split into an string array is a valid train string"""

    def check_train_string(self, stringList):
        if stringList.__len__() == 4:
                try:
                    speed = float(stringList[2])
                    cap = int(stringList[3])
                    return True
                except:
                    return False
        else:
            return False

    """Checks wether a input line split into an string array is a valid passengers string"""

    def check_passenger_string(self, stringList):
        if stringList.__len__() == 5:
                try:
                    groupSize = int(stringList[3])
                    time = int(stringList[4])
                    return True
                except:
                    return False
        else:
            return False



    """Parses stations, lanes, trains and passengers from input and returns a list of those objects as list."""

    def parse_input(self):
        #TODO Exception handling in output_parser
         #old
         #   objects = [self.parse_stations(), self.parse_lines(), self.parse_trains(), self.parse_passengers()]

            #new
            station_array = self.parse_stations()
            train_array = self.parse_trains(station_array)
            line_array = self.parse_lines(station_array)
            passenger_array = self.parse_passengers(station_array)

            #delte this later:
            for i in station_array:
                print(i.to_string())
            for i in train_array:
                print(i.to_string())
            for i in line_array:
                print(i.to_string())
            for i in passenger_array:
                print(i.to_string())


            objects = [station_array, self.parse_lines(station_array), self.parse_trains(station_array), self.parse_passengers(station_array)]
            return objects

