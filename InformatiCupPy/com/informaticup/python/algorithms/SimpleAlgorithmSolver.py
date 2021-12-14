from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
import sys


class SimpleAlgorithmSolver(ISolver):
    """ Example solver-class. """

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lanes = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]

    def solve(self, input):
        while self.check_break_condition():
            if self.check_free_train():
                focused_passenger = self.choose_next_passenger()
                chosen_train = self.check_free_train(passenger_group_size=focused_passenger.group_size)

    def check_break_condition(self):
        for passenger in self.passengers:
            if passenger.target_station != passenger.position:
                return True
        return False

    def check_free_train(self, passenger_group_size=0):
        for train in self.trains:
            if train.capacity - passenger_group_size > 0:
                return train  # train should be chosen better - maybe by using dijkstra?

    def choose_next_passenger(self):
        next_passenger = Passenger(sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize)
        for passenger in self.passengers:
            if passenger.target_time < next_passenger.target_time:
                next_passenger = passenger
        return next_passenger

    def get_name(self):
        return "simple-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
