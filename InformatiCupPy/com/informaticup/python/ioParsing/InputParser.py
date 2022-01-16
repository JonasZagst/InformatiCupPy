from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotParseInputException
from InformatiCupPy.com.informaticup.python.objects.Line import Line
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.objects.Station import Station
from InformatiCupPy.com.informaticup.python.objects.Train import Train


class InputParser:

    def __init__(self, input_path):
        self.input = open(input_path).read().split("\n")

    def parse_stations(self):
        """
        This method creates all station objects with the information given in the input file
        :return: list of station objects
        """

        stations_original = []
        stations = []
        counter = 0
        station = False

        # iterating over each line of our input file
        for i, line in enumerate(self.input):
            # setting the parsing boolean to "False", if the station segment ends
            if line == ("[Lines]") or line == ("[Trains]") or line == ("[Passengers]"):
                station = False
            # try to parse a line if it is in a station section
            if station:
                # splitting the line in order to get a string array, which is needed for the check method
                splitted_line = line.split(" ")

                # if this line is a valid station string, create a station object with the given values
                if self.check_station_string(splitted_line):
                    stations_original.append(Station(splitted_line[0], splitted_line[1]))
                # checking if it is another valid string
                elif line.startswith("#") or line == "" or line == "[Trains]" or line == "[Lines]" or\
                     line == "[Stations]" or line == "[Passengers]":
                    continue
                # if it is not another valid string, raise this exception, because there is a format problem in the file
                else:
                    raise CannotParseInputException()
            # setting the parsing boolean to "True" if a station segment begins
            if line == "[Stations]":
                station = True

        # setting the actually used IDs
        for s in stations_original:
            counter += 1
            s.set_internal_id("S" + str(counter))
            stations.append(s)

        return stations

    def parse_lines(self, station_array):
        """
        This method creates all line objects with the information given in the input file
        :return: list of line objects
        """

        lines_original = []
        lines = []
        counter = 0
        line_bool = False

        # iterating over each line of our input file
        for i, line in enumerate(self.input):
            # setting the parsing boolean to "False" if the line segment ends
            if line == ("[Stations]") or line == ("[Trains]") or line == ("[Passengers]"):
                line_bool = False
            # try to parse this line, if it is in a line segment
            if line_bool:
                # split the line in order to get the string array needed for the check method
                splitted_line = line.split(" ")

                # creating a line object, if it is a valid line string
                if self.check_line_string(splitted_line):
                    connected_stations = [splitted_line[1], splitted_line[2]]
                    lines_original.append(Line(splitted_line[0], connected_stations, splitted_line[3],
                                               splitted_line[4]))
                # if it is not a valid line string, check if it is another valid line
                elif line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or \
                     line == "[Passengers]" or line == "":
                    continue
                # if it is not a valid line, raise tis exception, because there is a format problem in our input file
                else:
                    raise CannotParseInputException()
            # setting the parsing boolean to "True" if a line segment begins
            if line == "[Lines]":
                line_bool = True

        # setting the actually used IDs
        for li in lines_original:
            counter = counter + 1
            li.set_internal_id("L" + str(counter))
            original_stations = li.get_original_connected_stations()
            internal_stations = []
            first_station = ""
            second_station = ""

            # replace the original station IDs used in the original string with the internal IDs of the used stations
            for st in station_array:

                if str(st.get_original_id()) == (original_stations[0]):
                    first_station = st.get_internal_id()
                elif str(st.get_original_id()) == (original_stations[1]):
                    second_station = st.get_internal_id()

            internal_stations.append(first_station)
            internal_stations.append(second_station)

            li.set_internal_connected_stations(internal_stations)
            lines.append(li)

        return lines

    def parse_trains(self, station_array):
        """
        This method creates all train objects with the information given in the input file
        :return: list of train objects
        """

        trains_original = []
        trains = []
        train = False
        counter = 0

        # iterate over each line of our input file
        for i, line in enumerate(self.input):
            # setting the parsing boolean to "False" if the train segment ends
            if line == ("[Stations]") or line == ("[Lines]") or line == ("[Passengers]"):
                train = False
            # try to parse the line if it is in a train segment
            if train:
                # split the line in order to get a string array, which is needed for the check method
                splitted_line = line.split(" ")

                # create a train object with the given information if it is a valid train string
                if self.check_train_string(splitted_line):
                    trains_original.append(Train(splitted_line[0], splitted_line[1], splitted_line[2],
                                                 splitted_line[3]))
                # if it is not a valid train string, check whether it is another valid string
                elif line.startswith(
                    "#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or \
                        line == "[Passengers]" or line == "":
                    continue
                # if it is not a valid string, raise this exception, because there is a format problem in our input file
                else:
                    raise CannotParseInputException()
            # setting the parsing boolean to "True" if a train segment starts
            if line == "[Trains]":
                train = True

        # setting the actually used IDs
        for t in trains_original:
            counter = counter + 1
            t.set_internal_id("T" + str(counter))

            # if the train is free positionable, just set the internal ID to "*"
            if t.get_original_position() == "*":
                t.set_internal_position("*")
                trains.append(t)
                continue
            # if it is not free positionable, just replace the original station ID by the internal station ID
            else:
                for st in station_array:

                    if str(st.get_original_id()) == (str(t.get_original_position())):
                        t.set_internal_position(st.to_string().split(" ")[0])

            trains.append(t)

        return trains

    def parse_passengers(self, station_array):
        """
        This method creates all passenger objects with the information given in the input file
        :return: list of passenger objects
        """

        passengers_original = []
        passengers = []
        counter = 0
        passenger = False

        # iterating over each line of our input file
        for i, line in enumerate(self.input):
            # setting the parsing boolean to "False" if the passenger segment ends
            if line == ("[Stations]") or line == ("[Trains]") or line == "[Lines]":
                passenger = False
            # try to parse the line if it is in a passenger segment
            if passenger:
                # split the line in order to get a string array, which is needed for the check method
                splitted_line = line.split(" ")

                # creating a passenger object with the given information if it is a valid passenger string
                if self.check_passenger_string(splitted_line):
                    passengers_original.append(Passenger(splitted_line[0],
                                                         splitted_line[1],
                                                         splitted_line[2],
                                                         splitted_line[3],
                                                         splitted_line[4]))
                # check whether it is another valid string
                elif line.startswith("#") or line == "[Stations]" or line == "[Trains]" or line == "[Lines]" or \
                     line == "[Passengers]" or line == "":
                    continue
                # if it is not a valid string, raise this exception, because there is a format problem in our input file
                else:
                    raise CannotParseInputException()
            # setting the parsing boolean to "True" if a passenger segment starts
            if line == "[Passengers]":
                passenger = True

        # setting the actually used IDs
        for p in passengers_original:
            counter = counter + 1
            p.set_internal_id("P" + str(counter))

            # replace the original station IDs with the internal IDs
            for st in station_array:
                if str(st.get_original_id()) == (str(p.get_original_initial_station())):
                    p.set_initial_station(st.to_string().split(" ")[0])
                elif str(st.get_original_id()) == (str(p.get_original_target_station())):
                    p.set_target_station(st.to_string().split(" ")[0])

            passengers.append(p)

        return passengers

    def check_station_string(self, string_list):
        """
        This method checks, whether a String array is a valid information provider for a station object
        :return: If it is a valid True, else False
        """

        # a station string has only two elements, if there are not two elements, return "False"
        if string_list.__len__() == 2:
            # try to cast the elements, which need to be numbers in order to figure out, whether they are valid
            try:
                cap = int(string_list[1])

                return True
            except:
                return False
        else:
            return False

    def check_line_string(self, string_list):
        """
        This method checks, whether a String array is a valid information provider for a line object
        :return: If it is a valid True, else False
        """

        # a line string has only five elements, if there are not five elements, return "False"
        if string_list.__len__() == 5:
            # try to cast the elements, which need to be numbers in order to figure out, whether they are valid
            try:
                length = float(string_list[3])
                cap = int(string_list[4])

                return True
            except:
                return False
        else:
            return False

    def check_train_string(self, string_list):
        """
        This method checks, whether a String array is a valid information provider for a train object
        :return: If it is a valid True, else False
        """

        # a train string has only four elements, if there are not four elements, return "False"
        if string_list.__len__() == 4:
            # try to cast the elements, which need to be numbers in order to figure out, whether they are valid
            try:
                speed = float(string_list[2])
                cap = int(string_list[3])

                return True
            except:
                return False
        else:
            return False

    def check_passenger_string(self, string_list):
        """
        This method checks, whether a String array is a valid information provider for a passenger object
        :return: If it is a valid True, else False
        """

        # a passenger string has only five elements, if there are not five elements, return "False"
        if string_list.__len__() == 5:
            # try to cast the elements, which need to be numbers in order to figure out, whether they are valid
            try:
                groupSize = int(string_list[3])
                time = int(string_list[4])

                return True
            except:
                return False
        else:
            return False

    def parse_input(self):
        """
        This method reads the input file in order to crate all objects
        :return: list of lists, which contains all objects
        """
        station_array = self.parse_stations()
        objects = [station_array, self.parse_lines(station_array), self.parse_trains(station_array),
                   self.parse_passengers(station_array)]

        return objects
