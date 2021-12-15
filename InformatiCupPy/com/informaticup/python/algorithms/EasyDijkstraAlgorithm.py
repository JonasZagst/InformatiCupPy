import math
from collections import deque

from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver


class EasyDijkstraAlgorithm(ISolver):

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]

    def solve(self, input):
        # TODO: write (doc)comments for methods
        file_solvable = True
        time = 0

        # setting up the Graph
        graph = Graph()
        for s in self.stations:
            graph.add_node(s.id)
        for l in self.lines:
            graph.add_edge(l.connected_stations[0], l.connected_stations[1], int(l.length), l.id)

        # only for demo reasons
        print(self.calculateShortestPath(graph, 'S2', 'S6'))

        # care for wildcard trains
        if not self.trains[0].fixed_start:
            # check if there is enough space in the whole graph for an additional wildcard train
            stations_with_capacity = 0
            for s in self.stations:
                if self.check_station_capacity(s) >= 1:
                    stations_with_capacity += 1

            if stations_with_capacity < 1:
                file_solvable = False
            train_placed = False

            # first check for initial station of the first passenger
            for s in self.stations:
                if s.id == self.passengers[0].initial_station and self.check_station_capacity(s) >= 1:
                    initial_position = self.passengers[0].initial_station
                    self.trains[0].initial_position = initial_position
                    self.trains[0].position = initial_position
                    train_placed = True
                    break

            # evaluate capacity of all other stations
            if not train_placed:
                for s in self.stations:
                    if self.check_station_capacity(s) >= 1:
                        initial_position = s.id
                        self.trains[0].initial_position = initial_position
                        self.trains[0].position = initial_position
                        break

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
                        length, list_of_path, list_of_lines = self.calculateShortestPath(graph, self.trains[0].position,
                                                                                         p.initial_station)
                        time = self.travelSelectedPath(time, list_of_path, list_of_lines, self.trains[0], None)

                    # getting the passenger to his target station
                    if self.trains[0].position == p.initial_station:
                        length, list_of_path, list_of_lines = self.calculateShortestPath(graph, self.trains[0].position,
                                                                                         p.target_station)
                        p.journey_history[time] = self.trains[0].id
                        time += 1
                        time = self.travelSelectedPath(time, list_of_path, list_of_lines, self.trains[0], p)
                        p.journey_history[time] = "Detrain"
                        time += 1
                    else:
                        # TODO: Calculate individual delay
                        print("something went wrong... your train didn't travel to the passenger")
        else:
            print("Input file is not solvable")

    def calculateShortestPath(self, graph, start, target):
        visited, paths, names = self.dijkstra(graph, start)
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

    # calculates the shortest distance of every node to the initial node in the given graph
    # inspired by: https://gist.github.com/mdsrosa/c71339cb23bc51e711d8
    @staticmethod
    def dijkstra(graph, initial):
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
        count = 0

        # putting station objects in instead of id's in resulting string of shortest path algorithm
        for n, i in enumerate(list_of_path):
            for s in self.stations:
                if s.id == i:
                    list_of_path[n] = s

        for visited_lines in list_of_lines:
            count += 1
            for all_lines in self.lines:
                if all_lines.id == visited_lines:
                    visited_lines = all_lines
                    train.journey_history[int(time)] = visited_lines.id
                    time_temp = float(visited_lines.length)/float(train.speed)
                    time += int(math.ceil(time_temp))
                    if self.check_station_capacity(list_of_path[count]) < 1:
                        # TODO: evaluate capacity --> idea: train from goal station meets train[0] in last round before arriving
                        # TODO: not working yet for multi lane use
                        self.check_trains_at_station(list_of_path[count])[0].journey_history[int(time)-1] = visited_lines.id
                        self.check_trains_at_station(list_of_path[count])[0].position = list_of_path[count]
                    train.position = list_of_path[count].id
                    if passenger is not None:
                        passenger.position = list_of_path[count].id
                    break

        return int(time)

    def check_trains_at_station(self, station):
        trains_at_station = []
        for t in self.trains:
            if t.position == station.id:
                trains_at_station.append(t)
        return trains_at_station

    def check_station_capacity(self, station):
        return int(station.capacity) - len(self.check_trains_at_station(station))

    def get_name(self):
        return "easy-dijkstra-algoritm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
