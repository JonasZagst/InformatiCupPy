from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from InformatiCupPy.com.informaticup.python.algorithms.EasyDijkstraAlgorithm import EasyDijkstraAlgorithm
import sys


class SimpleAlgorithmSolver(ISolver):
    """ Simple algorithm to solve an input problem. ----- not completely implemented yet -----
        Works by looping through the passengers in the order of the their priority/target time.
        Uses dijkstra algorithm for shortest path problems. """

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lanes = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]

    def solve(self, input):
        """ Method to solve an input problem.
            input: input list (result of Input_Parser.parse_input())"""
        # setting up the Graph
        graph = Graph()
        for station in self.stations:
            graph.add_node(station.id)
        for lane in self.lanes:
            graph.add_edge(lane.connected_stations[0], lane.connected_stations[1], int(lane.length), lane.id)

        # starting solving algorithm
        while self.check_break_condition():
            if self.check_free_train():
                focused_passenger = self.choose_next_passenger()
                chosen_train = self.check_free_train(passenger_group_size=focused_passenger.group_size)
                _length, _stations, _lanes = EasyDijkstraAlgorithm.dijkstra(graph, chosen_train.position)

                # for demo reasons:
                break

    def check_break_condition(self):
        """ Checks if the main loop of the algorithm can finish/stop.
            Returns True as long as there are still passengers who haven't reached their target station yet.
            Return False if all passengers have already reached their target station. """
        for passenger in self.passengers:
            if passenger.target_station != passenger.position:
                return True
        return False

    def check_free_train(self, passenger_group_size=0):
        """ Checks if there is a free train (train that has enough capacity left for a specific group of passengers).
            Returns nothing if there is no train that fulfills this condition.
            Returns, if there is a train to fulfill the condition, this very train.
            (currently: first train that fulfills condition; better: nearest train)
            passenger_group_size: size of the passenger group that should fit into the train."""
        for train in self.trains:
            if int(train.capacity) - int(passenger_group_size) >= 0:
                return train  # train should be chosen better - maybe by using dijkstra?

    def choose_next_passenger(self):
        """ Chooses the next passenger with should be brought to its target station.
            Chooses the passenger whose target_time is the lowest (only passengers that haven't reached their
            target station yet can be chosen).
            Returns the chosen passenger. """
        next_passenger = Passenger(sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize)
        for passenger in self.passengers:
            if int(passenger.target_time) < int(next_passenger.target_time) \
                    and passenger.target_station != passenger.position:
                next_passenger = passenger
        return next_passenger

    def get_name(self):
        return "simple-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
