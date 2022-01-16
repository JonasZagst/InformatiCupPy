import math
from collections import deque

from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotSolveInput, CannotBoardPassenger
from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper


class SimpleDijkstraAlgorithm(ISolver):
    """ Primitive Algorithm, which iterates through a list of all passengers and uses one train to bring them
    separately to their distinct destinations. To calculate the shortest path between two stations the
    dijkstra algorithm is used.
    The algorithm also features a handling of wildcard trains, passenger/station/line capacity evaluation
    and calculation of cumulated delay of all passengers
    Weakness: doesn't prioritize passengers and carries only one passenger at the same time
    """

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]

    def solve(self):
        """
        Method to solve an input problem. To understand the general thoughts this algorithm is based on read
        the class description. To comprehend the separate steps have a look at the comments.
        :return: cumulated delay time of all passengers
        """
        file_solvable = True
        time = 0
        delay_cumulated = 0

        self.trains.sort(key=lambda x: x.capacity, reverse=True)

        # check if wildcards can be placed
        station_capacity_cumulated = 0
        for s in self.stations:
            station_capacity_cumulated += self.check_station_capacity(s)

        # remove wildcard trains if they cannot be placed
        if station_capacity_cumulated == 0 and (not self.trains[0].fixed_start):
            for t in reversed(self.trains):
                if not t.fixed_start:
                    self.trains.remove(t)

        # setting up the Graph
        graph = Helper.set_up_graph(self.stations, self.lines)

        try:
            my_train = self.trains[0]
        except:
            file_solvable = False

        # uses only one train to transport all passengers
        if file_solvable:
            # care for wildcard trains
            if not my_train.fixed_start:
                train_placed = False

                # first check for initial station of the first passenger
                for s in self.stations:
                    if s.id == self.passengers[0].initial_station and self.check_station_capacity(s) >= 1:
                        my_train.initial_position = self.passengers[0].initial_station
                        my_train.position = self.passengers[0].initial_station
                        train_placed = True
                        break

                # evaluate capacity of all other stations
                if not train_placed:
                    for s in self.stations:
                        if self.check_station_capacity(s) >= 1:
                            my_train.initial_position = s.id
                            my_train.position = s.id
                            break

            time = 1

            for p in self.passengers:
                # evaluate if passenger group fits into used train
                if my_train.capacity < p.group_size:
                    raise CannotSolveInput()
                else:
                    # moving train to passenger
                    if my_train.position != p.initial_station:
                        length, list_of_path, list_of_lines = self.calculate_shortest_path(graph,
                                                                                           my_train.position,
                                                                                           p.initial_station)
                        time = self.travel_selected_path(time, list_of_path, list_of_lines, my_train, None)

                    # getting the passenger to his target station
                    if my_train.position == p.initial_station:
                        length, list_of_path, list_of_lines = self.calculate_shortest_path(graph,
                                                                                           my_train.position,
                                                                                           p.target_station)
                        p.journey_history[time] = my_train.id
                        time += 1
                        time = self.travel_selected_path(time, list_of_path, list_of_lines, my_train, p)
                        p.journey_history[time] = "Detrain"
                        if time - int(p.target_time) > 0:
                            delay_cumulated += time - int(p.target_time)

                        time += 1
                    else:
                        raise CannotBoardPassenger()
        else:
            raise CannotSolveInput()

        return delay_cumulated

    @staticmethod
    def calculate_shortest_path(graph, start, target):
        """
        uses the dijkstra algorithm to calculate the shortest path from an initial station to all others
        and creates based on the return data an easy to read and handle output for one station
        :param graph: object, which represents all lines, stations and their corresponding edges
        :param start: station where the calculation should start
        :param target: station where the calculation should end
        :return: distance as whole, visited stations and visited lines
        """
        if start == target:
            return 0, list(target), list()

        visited, paths, names = SimpleDijkstraAlgorithm.dijkstra(graph, start)
        full_path = deque()
        full_names = deque()

        _target = paths[target]

        while _target != start:
            full_path.appendleft(_target)
            _start_target = _target
            _target = paths[_target]
            full_names.appendleft(names[_start_target, _target])

        full_path.appendleft(start)
        full_path.append(target)
        full_names.append(names[full_path[-2], full_path[-1]])

        return visited[target], list(full_path), list(full_names)

    # inspired by:
    @staticmethod
    def dijkstra(graph, initial):
        """
        calculates the shortest distance of every node to the initial node in the given graph using the
        well known dijkstra algorithm. This implementation is based on the implementation of mdsrosa, which can be
        found here: https://gist.github.com/mdsrosa/c71339cb23bc51e711d8 but was modified slightly to fit the use case
        :param graph: object, which represents all lines, stations and their corresponding edges
        :param initial: station where the calculation should start
        :return: list of visited stations, list of possible paths, list of line names
        """
        # lists every station and its distance to the initial node
        visited = {initial: 0}
        path = {}
        nodes = set(graph.nodes)

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            # calculates the distance to each adjacent node and evaluates if it means an improvement
            for edge in graph.edges[min_node]:
                try:
                    weight = current_weight + graph.distances[(min_node, edge)]
                except:
                    try:
                        weight = current_weight + graph.distances[(edge, min_node)]
                    except:
                        continue
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node

        names = graph.names

        return visited, path, names

    def travel_selected_path(self, time, list_of_path, list_of_lines, train, passenger):
        """
        Based on a given path this method realizes the travelling of passenger and train.
        :param time: start time of travelling process
        :param list_of_path: list of paths to visit (calculated before using the dijkstra algorithm)
        :param list_of_lines: list of lines to visit (calculated before using the dijkstra algorithm)
        :param train: train which would be used to travel
        :param passenger: passenger (also can be None) which is transported in the train
        :return: end time after travelling process
        """
        count = 0

        helper = Helper()

        # putting station objects in instead of id's in resulting string of shortest path algorithm
        try:
            for n, station_id in enumerate(list_of_path):
                s = helper.get_element_from_list_by_id(station_id, self.stations)
                list_of_path[n] = s
        except:
            print("caught")

        for visited_lines in list_of_lines:
            count += 1
            for all_lines in self.lines:
                if all_lines.id == visited_lines:
                    visited_lines = all_lines
                    train.journey_history[int(time)] = visited_lines.id
                    time_temp = float(visited_lines.length) / float(train.speed)
                    time += int(math.ceil(time_temp))
                    if self.check_station_capacity(list_of_path[count]) < 1:
                        self.check_trains_at_station(list_of_path[count])[0].journey_history[
                            int(time) - 1] = visited_lines.id
                        self.check_trains_at_station(list_of_path[count])[0].position = list_of_path[count]
                    train.position = list_of_path[count].id
                    if passenger is not None:
                        passenger.position = list_of_path[count].id
                    break

        return int(time)

    def check_trains_at_station(self, station):
        """
        checks how many trains are at a given station
        :param station: station object to inspect
        :return: number of trains at the inspected station
        """
        trains_at_station = []
        for t in self.trains:
            if t.position == station.id:
                trains_at_station.append(t)
        return trains_at_station

    def check_station_capacity(self, station):
        """
        checks how many capacity is left at a given station
        :param station: station object to inspect
        :return: number of free capacity slots at the inspected station
        """
        return int(station.capacity) - len(self.check_trains_at_station(station))

    def get_name(self):
        return "simple-dijkstra-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
