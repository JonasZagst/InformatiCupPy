from collections import defaultdict, deque


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.names = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance, name):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.names[(from_node, to_node)] = name
        self.names[(to_node, from_node)] = name


def dijkstra(graph, initial):
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
                try:
                    weight = current_weight + graph.distances[(edge, min_node)]
                except:
                    continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    names = graph.names

    return visited, path, names


def shortest_path(graph, origin, destination):
    if origin == destination:
        return 0, list(destination), list()

    visited, paths, names = dijkstra(graph, origin)
    full_path = deque()
    full_names = deque()
    print(names)

    _destination = paths[destination]
    while _destination != origin:
        full_path.appendleft(_destination)
        _start_destination = _destination
        _destination = paths[_destination]
        full_names.appendleft(names[_start_destination, _destination])

    full_path.appendleft(origin)
    full_path.append(destination)
    full_names.append(names[full_path[-2], full_path[-1]])

    return visited[destination], list(full_path), list(full_names)


if __name__ == '__main__':
    graph = Graph()

    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        graph.add_node(node)

    graph.add_edge('A', 'B', 10, 'L1')
    graph.add_edge('A', 'C', 20, 'L2')
    graph.add_edge('B', 'D', 15, 'L3')
    graph.add_edge('C', 'D', 30, 'L4')
    graph.add_edge('B', 'E', 50, 'L5')
    graph.add_edge('D', 'E', 30, 'L6')
    graph.add_edge('E', 'F', 5, 'L7')
    graph.add_edge('F', 'G', 2, 'L8')
    graph.add_edge('A', 'H', 7, 'L9')
    graph.add_edge('G', 'H', 2, 'L10')

    print(shortest_path(graph, 'A', 'D'))  # output: (25, ['A', 'B', 'D'])
