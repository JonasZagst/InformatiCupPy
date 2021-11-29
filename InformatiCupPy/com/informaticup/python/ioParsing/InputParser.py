from com.informaticup.python.objects.Lane import Lane
from com.informaticup.python.objects.Passenger import Passenger
from com.informaticup.python.objects.Station import Station
from com.informaticup.python.objects.Train import Train


class InputParser:

    def __init__(self, input_path):
        self.input = open(input_path, "r").read().split("\n")

    def parse_stations(self):
        stations = []
        station = False

        for i, line in enumerate(self.input):
            if line == "":
                station = False
            if station == True:
                station_str = line.split(" ")
                stations.append(Station(station_str[0], station_str[1]))
            if line == "[Stations]":
                station = True

        return stations

    def parse_lanes(self):
        lanes = []
        lane = False

        for i, line in enumerate(self.input):
            if line == "":
                lane = False
            if lane == True:
                lane_str = line.split(" ")
                connected_stations = [lane_str[1], lane_str[2]]
                lanes.append(Lane(lane_str[0], connected_stations, lane_str[3], lane_str[4]))
            if line == "[Lines]":
                lane = True

        return lanes

    def parse_trains(self):
        trains = []
        train = False

        for i, line in enumerate(self.input):
            if line == "":
                train = False
            if train == True:
                train_str = line.split(" ")
                trains.append(Train(train_str[0], train_str[1], train_str[2], train_str[3]))
            if line == "[Trains]":
                train = True
        return trains

    def parse_passengers(self):
        passengers = []
        passenger = False

        for i, line in enumerate(self.input):
            if line == "":
                passenger = False
            if passenger == True:
                passenger_str = line.split(" ")
                passengers.append(Passenger(passenger_str[0],
                                            passenger_str[1],
                                            passenger_str[2],
                                            passenger_str[3],
                                            passenger_str[4]))

            if line == "[Passengers]":
                passenger = True

        return passengers

    def parse_input(self):
        objects = [self.parse_stations(), self.parse_lanes(), self.parse_trains(), self.parse_passengers()]

        return objects