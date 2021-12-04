from InformatiCupPy.com.informaticup.python.algorithms.SimpleAlgorithmSolver import SimpleAlgorithmSolver
from InformatiCupPy.com.informaticup.python.ioParsing.InputParser import InputParser
from InformatiCupPy.com.informaticup.python.ioParsing.OutputParser import OutputParser
from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph
from collections import deque

def main():
    '''
    List order + each variables:
        1 Stations
            id, capacity
        2 Lanes
            id, connected_stations, length, capacity
        3 Trains
            id, capacity, speed, position
        4 Passengers
            id, initial_station, target_station, group_size, target_time
    '''

    # creates a list (length 4) of lists (length x), which contains several object parsed from the input file
    input = InputParser("../input-output/input.txt").parse_input()

    for i in input:
        for j in i:
            print(j.to_string())
    print(input)

    solvers = [SimpleAlgorithmSolver()]
    OutputParser.parse_output_files(solvers, input)


    stations = input[0]
    lanes = input[1]
    trains = input[2]
    passengers = input[3]

    algorithm1(stations, lanes, trains, passengers)


def algorithm1(stations, lanes, trains, passengers):
    output = ''

    # setting up the Graph
    graph = Graph()
    for s in stations:
        graph.add_node(s.id)
    for l in lanes:
        graph.add_edge(l.connected_stations[0], l.connected_stations[1], int(l.length))

    print(calculateShortestPath(graph, 'S6', 'S5'))

    # uses only one train to transport all passengers
    for p in passengers:
        # moving train to passenger
        if trains[0].position != p.initial_station:
            length, listOfPath = calculateShortestPath(graph, trains[0].position, p.initial_station)
            travelSelectedPath(length, listOfPath, trains[0].id, None)

        # getting the passenger to his target station
        if trains[0].position == p.initial_station:
            length, listOfPath = calculateShortestPath(graph, trains[0].position, p.target_station)
            travelSelectedPath(length, listOfPath, trains[0].id, p.id)
        else:
            print("something went wrong... your train didn't travel to the passenger")

    return output


def calculateShortestPath(graph, start, target):
    visited, paths = dijkstra(graph, start)
    full_path = deque()
    _target = paths[target]

    while _target != start:
        full_path.appendleft(_target)
        _target = paths[_target]

    full_path.appendleft(start)
    full_path.append(target)

    return visited[target], list(full_path)


# calculates the shortest distance of every node to the initial node in the given graph
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

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def travelSelectedPath(length, listOfPath, train, passenger):
    print("TODO")


main()
