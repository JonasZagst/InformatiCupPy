from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from collections import deque


class EasyDijkstraAlgorithm(ISolver):

    def solve(self, input):
        stations = input[0]
        lanes = input[1]
        trains = input[2]
        passengers = input[3]

        result = ""
        time = 0

        # setting up the Graph
        graph = Graph()
        for s in stations:
            graph.add_node(s.id)
        for l in lanes:
            graph.add_edge(l.connected_stations[0], l.connected_stations[1], int(l.length))

        # only for demo reasons
        print(self.calculateShortestPath(graph, 'S6', 'S2'))

        # uses only one train to transport all passengers
        for p in passengers:
            # moving train to passenger
            if trains[0].position != p.initial_station:
                length, listOfPath = self.calculateShortestPath(graph, trains[0].position, p.initial_station)
                result = result + "\n" + str(time) + " Depart " + trains[0].id
                time += self.travelSelectedPath(length, listOfPath, trains[0], None)

            # getting the passenger to his target station
            if trains[0].position == p.initial_station:
                length, listOfPath = self.calculateShortestPath(graph, trains[0].position, p.target_station)
                result = result + "\n" + str(time) + " Board " + trains[0].id
                time += 1
                result = result + "\n" + str(time) + " Depart " + trains[0].id
                time += self.travelSelectedPath(length, listOfPath, trains[0], p)
                result = result + "\n" + str(time) + " Detrain " + trains[0].id
                time +=1
                if p.position == p.target_station:
                    print("Passenger " + p.id + " arrived at "+ p.position)
            else:
                print("something went wrong... your train didn't travel to the passenger")

        return result


    def calculateShortestPath(self, graph, start, target):
        visited, paths = self.dijkstra(graph, start)
        full_path = deque()
        _target = paths[target]

        while _target != start:
            full_path.appendleft(_target)
            _target = paths[_target]

        full_path.appendleft(start)
        full_path.append(target)

        return visited[target], list(full_path)

    # calculates the shortest distance of every node to the initial node in the given graph
    # inspired by: https://gist.github.com/mdsrosa/c71339cb23bc51e711d8
    def dijkstra(self, graph, initial):
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

        return visited, path

    def travelSelectedPath(self, length, listOfPath, train, passenger):
        '''
        just an easy implementation of this method to serve this primitive algorithm
        (only cares about start and target without iterating through the whole path)
        '''
        train.position = listOfPath[-1]
        if (passenger is not None):
            passenger.position = listOfPath[-1]
        time = length/int(train.speed)

        return int(time)

    def get_name(self):
        return "easy-dijkstra-algoritm"

    def flush(self):
        pass
