import copy
import math
import sys
from collections import deque

from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper
from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotSolveInput, CannotBoardPassenger


class AdvancedDijkstraAlgorithm(ISolver):

    # TODO: improve the easy version of this algorithm with the following ideas:
    #  - (implement the ability of trains to pass a station without stopping to save some time)
    #  - don't deliver passengers to early -> detrain them intelligent in the middle of the journey
    #  - capacity of lines/stations should also be changed (like train capacity) -> goal: use more than one train
    #  - take passengers with you when swapping - take passengers just with you for just a part of the journey

    def __init__(self, input_from_file, capacity_speed_ratio):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]
        self.capacity_speed_ratio = capacity_speed_ratio

    def solve(self):
        """
        Method to solve an input problem. To understand the general thoughts this algorithm is based on read
        the class description. To comprehend the separate steps have a look at the comments.
        """
        file_solvable = False
        time = 0
        delay_cumulated = 0

        # TODO: do all train evaluation on a deepcopy of self.trains to avoid problems with check_station_capacity method

        # get biggest passenger group
        self.passengers.sort(key=lambda x: x.group_size)
        biggest_passenger_group = self.passengers[0].group_size

        # prioritize passengers/trains
        self.passengers.sort(key=lambda x: x.target_time)

        # setting up the graph and a path dictionary
        graph = Helper.set_up_graph(self.stations, self.lines)
        path_dict = Helper.set_up_path_dict(self.stations)



        my_train, file_solvable = self.get_my_train(copy.deepcopy(self.trains), biggest_passenger_group, self.capacity_speed_ratio)

        time = 1

        # uses only one train to transport all passengers
        if file_solvable:
            for p in self.passengers:
                # evaluate passenger group size
                if my_train.capacity < p.group_size:
                    raise CannotSolveInput()
                elif p.position != p.target_station:
                    # moving train to passenger
                    if my_train.position != p.initial_station:
                        length, list_of_path, list_of_lines, path_dict = self.calculate_shortest_path(graph,
                                                                                                      my_train.position,
                                                                                                      p.initial_station,
                                                                                                      path_dict)
                        time, delay = self.travelSelectedPath(time, list_of_path, list_of_lines, my_train, None)
                        delay_cumulated += delay

                    # getting the passenger to his target station
                    if my_train.position == p.initial_station:
                        length, list_of_path, list_of_lines, path_dict = self.calculate_shortest_path(graph,
                                                                                                      my_train.position,
                                                                                                      p.target_station,
                                                                                                      path_dict)

                        time, delay = self.travelSelectedPath(time, list_of_path, list_of_lines, my_train, p)
                        delay_cumulated += delay

                    else:
                        raise CannotBoardPassenger()
        else:
            raise CannotSolveInput()

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
            return 0, list(target), list(), None

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
        delay_cumulated = 0
        passengers = []

        passengers_at_path = self.find_passengers_along_the_way(list_of_path)

        # for key, value in passengers_at_path.items():
        #     print(key, end=' ')
        #     for v in value:
        #         print(v.id, end=' ')
        #     print(' ')
        #
        # print("path finished")

        # replacing id's with objects
        for n, station_id in enumerate(list_of_path):
            s = Helper.get_element_from_list_by_id(station_id, self.stations)
            list_of_path[n] = s

        for n, line_id in enumerate(list_of_lines):
            l = Helper.get_element_from_list_by_id(line_id, self.lines)
            list_of_lines[n] = l

        for visited_lines in list_of_lines:

            if count == 0:
                boarded = False
                if list_of_path[count].id in passengers_at_path:
                    for p in passengers_at_path[list_of_path[count].id]:
                        passengers.append(p)
                    passengers.sort(key=lambda x: x.target_time)
                for p in passengers:
                    if not p.is_in_train and train.capacity >= p.group_size:
                        p.journey_history[time] = train.id
                        train.capacity = train.capacity - p.group_size
                        p.is_in_train = True
                        boarded = True
                if boarded:
                    time += 1

            for p in reversed(passengers):
                if not p.is_in_train:
                    passengers.remove(p)

            detrained = False
            boarded = False
            jumped = False

            count += 1
            train.journey_history[int(time)] = visited_lines.id
            time_temp = float(visited_lines.length) / float(train.speed)
            time_old = time
            if int(math.ceil(time_temp)) - 1 == 0:
                time += int(math.ceil(time_temp))
            else:
                time += int(math.ceil(time_temp)) - 1
                jumped = True
            # Swapping to handle capacity issues
            if self.check_station_capacity(list_of_path[count]) < 1:
                self.check_trains_at_station(list_of_path[count])[0].journey_history[
                    int(time_old + int(math.ceil(time_temp)) - 1)] = visited_lines.id
                self.check_trains_at_station(list_of_path[count])[0].position = list_of_path[count]
            train.position = list_of_path[count].id

            if list_of_path[count].id in passengers_at_path:
                for p in passengers_at_path[list_of_path[count].id]:
                    passengers.append(p)
                passengers.sort(key=lambda x: x.target_time)

            for p in passengers:
                if not p.is_in_train and train.capacity >= p.group_size:
                    if jumped:
                        p.journey_history[time + 1] = train.id
                    else:
                        p.journey_history[time] = train.id
                    train.capacity = train.capacity - p.group_size
                    p.is_in_train = True
                    boarded = True
                elif p.position != p.target_station and not p.reached_target and p.is_in_train:
                    p.position = list_of_path[count].id

                if p.position == p.target_station and not p.reached_target:
                    train.capacity = train.capacity + p.group_size
                    if time - int(p.target_time) > 0:
                        delay_cumulated += time - int(p.target_time)
                    p.reached_target = True
                    detrained = True
                    if jumped:
                        p.journey_history[time+1] = "Detrain"
                    else:
                        p.journey_history[time] = "Detrain"

            if (detrained or boarded) and jumped:
                time += 2
            elif detrained or boarded or (count == len(list_of_lines) and jumped):
                time += 1

        return int(time), int(delay_cumulated)

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

    def find_common_shortest_paths(self, shortest_paths):
        # TODO: write algorithm to find small subsets of common shortest paths in the list of lists
        i = 0

    def find_passengers_along_the_way(self, list_of_path):
        passengers_at_path = {}
        passengers = self.passengers

        for p in passengers:
            if p.initial_station in list_of_path and p.target_station in list_of_path \
                    and list_of_path.index(p.initial_station) < list_of_path.index(p.target_station) \
                    and not p.reached_target:
                if not (p.initial_station in passengers_at_path):
                    passengers_at_path[p.initial_station] = [p]
                else:
                    passengers_at_path[p.initial_station].append(p)

        return passengers_at_path

    def get_my_train(self, trains, biggest_passenger_group, capacity_speed_ratio):
        # check if wildcards can be placed
        station_capacity_cumulated = 0
        for s in self.stations:
            station_capacity_cumulated += self.check_station_capacity(s)

        # remove wildcard trains if they cannot be placed
        if station_capacity_cumulated == 0:
            for t in reversed(trains):
                if not t.fixed_start:
                    trains.remove(t)

        for train in reversed(trains):
            if train.capacity < biggest_passenger_group:
                trains.remove(train)

        trains.sort(key=lambda x: (x.capacity, x.speed))
        old_speed = trains[len(trains)-1].speed - 1
        for train in reversed(trains):
            if train.speed <= old_speed:
                trains.remove(train)
            else:
                old_speed = train.speed

        my_train = trains[int(capacity_speed_ratio*(len(trains)-1))]

        my_train = Helper.get_element_from_list_by_id(my_train.id, self.trains)

        train_placed = True

        if not my_train.fixed_start:
            train_placed = False
            # first check for initial station of the first passenger to save some time
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
                        train_placed = True
                        break

        if train_placed:
            file_solvable = True

        return my_train, file_solvable

    def get_name(self):
        """
        name of the algorithm (used to name the output file)
        :return: name of the algorithm
        """
        return f"advanced-dijkstra-algorithm-{str(self.capacity_speed_ratio)}"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
