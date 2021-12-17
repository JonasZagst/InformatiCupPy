from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from InformatiCupPy.com.informaticup.python.algorithms.EasyDijkstraAlgorithm import EasyDijkstraAlgorithm as Dij
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
            :param input: input list (result of Input_Parser.parse_input())
        """
        # setting up the Graph
        graph = Graph()
        for station in self.stations:
            graph.add_node(station.id)
        for lane in self.lanes:
            graph.add_edge(lane.connected_stations[0], lane.connected_stations[1], int(lane.length), lane.id)

        # starting solving algorithm
        while self.check_break_condition():
            if self.get_free_trains():
                focused_passenger = self.choose_next_passenger()
                chosen_train = self.get_nearest_possible_train(passenger=focused_passenger, graph=graph)
                if focused_passenger.position != chosen_train.position:
                    _length, _stations, _lanes = \
                        Dij.calculate_shortest_path(graph, focused_passenger.position, chosen_train.position)

                # for demo reasons:
                break

    def check_break_condition(self):
        """ Checks if the main loop of the algorithm can finish/stop.
            :return True, as long as there are still passengers who haven't reached their target station yet.
            :return False, if all passengers have already reached their target station.
        """
        for passenger in self.passengers:
            if passenger.target_station != passenger.position:
                return True
        return False

    def get_free_trains(self, passenger=None):
        """ Checks if there are free trains (trains that have enough capacity left for a specific group of passengers)
            and returns them.
            :param passenger: optional parameter, passenger that should fit into the train.
            :return: a list of all trains that fulfill the condition (empty list if no train fulfills condition).
        """
        possible_trains = []
        group_size = 0 if passenger is None else passenger.group_size
        for train in self.trains:
            if int(train.capacity) - int(group_size) >= 0:
                possible_trains.append(train)
        return possible_trains

    def get_nearest_possible_train(self, passenger=None, graph=None):
        """ Gets the nearest train that can take the passenger (by means of group size).
            Uses dijkstra shortest-path-calculation to identify the nearest train.
            :param passenger: passenger that shall use the train (needed for size check and path calculation).
            :param graph: Graph object of the input map.
            :return: nearest train.
        """
        possible_trains = self.get_free_trains(passenger=passenger)
        try:
            best_train = (possible_trains[0], sys.maxsize)  # tuple: (train, distance of train to passenger)
        except IndexError:
            return

        for p_train in possible_trains:
            if p_train.position == passenger.position:  # if there is a train that has already the same position
                # as the passenger, return that train
                return p_train
            # else calculate shortest path:
            distance_to_passenger, _, __ = Dij.calculate_shortest_path(graph, p_train.position, passenger.position)
            if distance_to_passenger < best_train[1]:
                best_train = (p_train, distance_to_passenger)

        return best_train

    def choose_next_passenger(self):
        """ Chooses the next passenger with should be brought to its target station.
            Chooses the passenger whose target_time is the lowest (only passengers that haven't reached their
            target station yet can be chosen).
            Returns the chosen passenger.
        """
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
