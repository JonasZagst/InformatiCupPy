import copy
import math
import sys
from collections import deque

from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper
from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotSolveInput, CannotBoardPassenger


class AdvancedPassengerParallelizationAlgorithm(ISolver):
    """ Algorithm, which iterates through a list of all passengers and uses one train to bring them
        to their distinct destinations. If there are passengers on the way, which want to travel to a target also
        on the path they can be took along. This selection of the train based on a parameter.
        To calculate the shortest path between two stations the dijkstra algorithm is used.
        The algorithm also features a handling of wildcard trains, passenger/station/line capacity evaluation
        and calculation of accumulated delay of all passengers
        Weakness: uses just one train to carry a passenger
        """

    def __init__(self, input_from_file, capacity_speed_ratio=0.5):
        """
        sets up the lists retrieved from the input
        :param input_from_file: list of all objects created by the input parser based on the input.txt
        :param capacity_speed_ratio: parameter to select train (has to be between 0 and 1)
            0: takes the fastest but smallest train possible
            1: takes the biggest but slowest train
        """
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]
        if 0 <= capacity_speed_ratio <= 1:
            self.capacity_speed_ratio = capacity_speed_ratio
        else:
            self.capacity_speed_ratio = 0.5

    def solve(self):
        """
        Method to solve an input problem. To understand the general thoughts this algorithm is based on read
        the class description. To comprehend the separate steps have a look at the comments.
        :return: cumulated delay time of all passengers
        """
        file_solvable = False
        time = 0
        delay_cumulated = 0

        # get biggest passenger group
        self.passengers.sort(key=lambda x: x.group_size)
        biggest_passenger_group = self.passengers[0].group_size

        # prioritize passengers/trains
        self.passengers.sort(key=lambda x: x.target_time)

        # setting up the graph and a path dictionary
        graph = Helper.set_up_graph(self.stations, self.lines)
        path_dict = Helper.set_up_path_dict(self.stations)

        # select train based on parameter
        my_train, file_solvable = self.get_my_train(copy.deepcopy(self.trains), biggest_passenger_group,
                                                    self.capacity_speed_ratio)

        time = 1

        # calculate shortest paths for all passengers
        passenger_dict = {}
        for p in self.passengers:
            list_of_path, list_of_lines, path_dict = self.calculate_shortest_path(graph, p.initial_station, p.target_station, path_dict)
            passenger_dict[p] = [list_of_path, list_of_lines]

        # uses only one train to transport all passengers
        if file_solvable:
            for p in self.passengers:
                # evaluate passenger group size
                if my_train.capacity < p.group_size:
                    raise CannotSolveInput()
                elif p.position != p.target_station:
                    # moving train to passenger
                    if my_train.position != p.position:
                        list_of_path, list_of_lines, path_dict = self.calculate_shortest_path(graph,
                                                                                                      my_train.position,
                                                                                                      p.position,
                                                                                                      path_dict)
                        time, delay = self.travel_selected_path(time, list_of_path, list_of_lines, my_train, passenger_dict)
                        delay_cumulated += delay

                    # getting the passenger to his target station
                    if my_train.position == p.position:
                        time, delay = self.travel_selected_path(time, passenger_dict[p][0], passenger_dict[p][1], my_train, passenger_dict)
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
        :param dict: contains already calculated paths to reduce time consumption
        :return: distance as whole, visited stations and visited lines
        """
        if start == target:
            return list(target), list(), None

        path_dict = dict

        # select already calculated paths
        if path_dict[start] is not None:
            visited = path_dict[start][0]
            paths = path_dict[start][1]
            names = path_dict[start][2]
        else:
            visited, paths, names = AdvancedPassengerParallelizationAlgorithm.dijkstra(graph, start)
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

        return list(full_path), list(full_names), path_dict

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

    def travel_selected_path(self, time, list_of_path, list_of_lines, train, passenger_dict):
        """
        Based on a given path this method realizes the travelling of passenger and train.
        :param time: start time of travelling process
        :param list_of_path: list of paths to visit (calculated before using the dijkstra algorithm)
        :param list_of_lines: list of lines to visit (calculated before using the dijkstra algorithm)
        :param train: train which would be used to travel
        :return: end time after travelling process
        """
        count = 0
        delay_cumulated = 0
        passengers = []

        passengers_at_path = self.find_passengers_along_the_way(list_of_path, passenger_dict)

        to_remove_path = {}
        to_remove_lines = {}

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
                swap_train = self.check_trains_at_station(list_of_path[count])[0]
                swap_start_time = int(time_old + int(math.ceil(time_temp)) - 1)
                swap_passengers_dict = self.find_passengers_along_the_way([list_of_path[count].id, list_of_path[count-1].id], passenger_dict)
                swap_passengers = []
                for key, value in swap_passengers_dict.items():
                    swap_passengers = value
                for swap_passenger in reversed(swap_passengers):
                    if swap_train.capacity >= swap_passenger.group_size:
                        swap_passenger.journey_history[swap_start_time-1] = swap_train.id
                        swap_train.capacity = swap_train.capacity - swap_passenger.group_size
                        swap_passenger.is_in_train = True
                    else:
                        swap_passengers.remove(swap_passenger)

                swap_train.journey_history[swap_start_time] = visited_lines.id
                swap_train.position = list_of_path[count]

                swap_end_time = swap_start_time + math.ceil(float(visited_lines.length) / float(swap_train.speed))

                for swap_passenger in swap_passengers:
                    swap_passenger.journey_history[swap_end_time] = "Detrain"
                    swap_passenger.position = list_of_path[count-1].id
                    swap_passenger.reached_target = True
                    swap_passenger.is_in_train = False


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
                elif p.position != p.interim_target and (not p.reached_interim_target or not p.reached_target) and p.is_in_train:
                    if isinstance(passenger_dict[p][1][0], str):
                        line_rm = visited_lines.id
                    else:
                        line_rm = visited_lines

                    if not (p in to_remove_lines):
                        to_remove_lines[p] = [line_rm]
                    else:
                        to_remove_lines[p].append(line_rm)

                    if isinstance(passenger_dict[p][0][0], str):
                        path_rm = p.position
                    else:
                        path_rm = Helper.get_element_from_list_by_id(p.position, self.stations)

                    if not (p in to_remove_path):
                        to_remove_path[p] = [path_rm]
                    else:
                        to_remove_path[p].append(path_rm)

                    p.position = list_of_path[count].id



                if p.position == p.interim_target and not p.reached_interim_target:
                    train.capacity = train.capacity + p.group_size
                    if time - int(p.target_time) > 0:
                        delay_cumulated += time - int(p.target_time)
                    p.reached_interim_target = True
                    if p.interim_target == p.target_station:
                        p.reached_target = True
                    detrained = True
                    if jumped:
                        p.journey_history[time+1] = "Detrain"
                        p.is_in_train = False
                    else:
                        p.journey_history[time] = "Detrain"
                        p.is_in_train = False

            if (detrained or boarded) and jumped:
                time += 2
            elif detrained or boarded or (count == len(list_of_lines) and jumped):
                time += 1


        for key, value in to_remove_lines.items():
            for v in value:
                passenger_dict[key][1].remove(v)

        for key, value in to_remove_path.items():
            for v in value:
                passenger_dict[key][0].remove(v)

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

    def find_passengers_along_the_way(self, list_of_path, passenger_dict):
        passengers_at_path = {}
        passengers = self.passengers

        for key, value in passenger_dict.items():
            if key.position in list_of_path[:-1] and not key.reached_target:
                target_value = key.position
                for station in value[0]:
                    if station in list_of_path:
                        if list_of_path.index(key.position) < list_of_path.index(station) and station != target_value \
                                and value[0].index(key.position) < value[0].index(station):
                            target_value = station

                if target_value != key.position:
                    key.interim_target = target_value
                    key.reached_interim_target = False
                    if not (key.position in passengers_at_path):
                        passengers_at_path[key.position] = [key]
                    else:
                        passengers_at_path[key.position].append(key)

        return passengers_at_path

    def get_my_train(self, trains, biggest_passenger_group, capacity_speed_ratio):
        """
        gets a train, which can carry all passengers based on a parameter
        :param trains: list of all trains
        :param biggest_passenger_group: integer indicating the group size of the biggest passenger group
        :param capacity_speed_ratio: parameter to select train (has to be between 0 and 1)
            0: takes the fastest but smallest train possible
            1: takes the biggest but slowest train
        :return: selected train, boolean that indicates if the file is solvable for this algorithm
        """
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

        if len(trains) == 0:
            return None, False

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
        return f"advanced-passenger-parallelization-algorithm-{str(self.capacity_speed_ratio)}"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
