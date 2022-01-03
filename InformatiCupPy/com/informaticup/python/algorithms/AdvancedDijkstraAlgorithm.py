import math
from collections import deque

from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper
from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver


class AdvancedDijkstraAlgorithm(ISolver):

    # TODO: improve the easy version of this algorithm with the following ideas:
    #  - implement the ability of trains to pass a station without stopping to save some time
    #  - passenger priority based on target time, group size
    #  - take more passengers in one train

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]

    def solve(self):
        """
        Method to solve an input problem. To understand the general thoughts this algorithm is based on read
        the class description. To comprehend the separate steps have a look at the comments.
        """
        file_solvable = False
        time = 0
        delay_cumulated = 0

        # prioritize passengers with low target_time by sorting the list
        self.passengers.sort(key=lambda x: x.target_time)

        # setting up the dictionary which will contain already calculated paths
        path_dict = {}

        for s in self.stations:
            path_dict[s.id] = None

        # setting up the graph
        graph = Helper.set_up_graph(self.stations, self.lines)

        train_placed = False

        mytrain = None

        # care if the used train is a wildcard train
        for train in self.trains:
            if train.fixed_start and not train_placed:
                mytrain = train
                train_placed = True

            if not train.fixed_start and not train_placed:

                # first check for initial station of the first passenger to save some time
                for s in self.stations:
                    if s.id == self.passengers[0].initial_station and self.check_station_capacity(s) >= 1:
                        initial_position = self.passengers[0].initial_station
                        train.initial_position = initial_position
                        train.position = initial_position
                        train_placed = True
                        break

                # evaluate capacity of all other stations
                if not train_placed:
                    for s in self.stations:
                        if self.check_station_capacity(s) >= 1:
                            initial_position = s.id
                            train.initial_position = initial_position
                            train.position = initial_position
                            train_placed = True
                            break

        if train_placed:
            file_solvable = True

        time = 1

        # uses only one train to transport all passengers
        if file_solvable:
            for p in self.passengers:
                # evaluate passenger group size
                if self.trains[0].capacity < p.group_size:
                    print("Passenger", p.id, "cannot be transported by the used train. "
                                             "It will be skipped, because this algorithm provides no "
                                             "optional solution.")
                else:
                    # moving train to passenger
                    if self.trains[0].position != p.initial_station:
                        length, list_of_path, list_of_lines, path_dict = self.calculate_shortest_path(graph,
                                                                                           self.trains[0].position,
                                                                                           p.initial_station, path_dict)
                        time = self.travelSelectedPath(time, list_of_path, list_of_lines, self.trains[0], None)

                    # getting the passenger to his target station
                    if self.trains[0].position == p.initial_station:
                        length, list_of_path, list_of_lines, path_dict = self.calculate_shortest_path(graph,
                                                                                           self.trains[0].position,
                                                                                           p.target_station, path_dict)
                        p.journey_history[time] = self.trains[0].id
                        time += 1
                        time = self.travelSelectedPath(time, list_of_path, list_of_lines, self.trains[0], p)
                        p.journey_history[time] = "Detrain"
                        if time - int(p.target_time) > 0:
                            delay_cumulated += time - int(p.target_time)

                        time += 1
                    else:
                        print("something went wrong... your train didn't travel to the passenger")
        else:
            print("Input file is not solvable with this algorithm")

        return delay_cumulated

    @staticmethod
    def calculate_shortest_path(graph, start, target, dict):
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

        path_dict = dict

        if path_dict[start] is not None:
            visited = path_dict[start][0]
            paths = path_dict[start][1]
            names = path_dict[start][2]
        else:
            visited, paths, names = AdvancedDijkstraAlgorithm.dijkstra(graph, start)
            path_dict[start] = [visited, paths, names]

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

        return visited[target], list(full_path), list(full_names), path_dict

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

    def travelSelectedPath(self, time, list_of_path, list_of_lines, train, passenger):
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
        for n, station_id in enumerate(list_of_path):
            s = helper.get_element_from_list_by_id(station_id, self.stations)
            list_of_path[n] = s

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
        """
        name of the algorithm (used to name the output file)
        :return: name of the algorithm
        """
        return "advanced-dijkstra-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]

