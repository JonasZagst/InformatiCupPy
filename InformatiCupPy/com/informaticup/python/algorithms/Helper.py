from InformatiCupPy.com.informaticup.python.algorithms.Graph import Graph


class Helper:
    @staticmethod
    def get_element_from_list_by_id(element_id, list_):
        """ Easy way to get an object (Train, Passenger, Line or Station) from its respective id.
            Sorts list by id, calculates index = id - 1 and gets element from list at index = index.
            More efficient than using a for-each-loop each time a object for a given id is needed.
            :param element_id: id of the object you want to get (e.g. 'S1' or 'P12')
            :param list_: list of all stations/lines/trains/passengers, depending on what kind of object you search for
            :returns searched object (as Train/Passenger/Line/Passenger-Object)
        """
        list_.sort(key=lambda x: int(x.id[1:]))
        index = int(element_id[1:]) - 1
        return list_[index]

    @staticmethod
    def set_up_graph(stations, lines):
        """ Method to set up a graph. Needed each time the dijkstra-shortest-path calculation is used.
            :param stations: list of all stations (usually self.stations).
            :param lines: list of all lines (usually self.lines).
            :returns: the corresponding graph (built of the stations and lines) as Graph-Object.
        """
        graph = Graph()
        for station in stations:
            graph.add_node(station.id)
        for line in lines:
            graph.add_edge(line.connected_stations[0], line.connected_stations[1], float(line.length), line.id)
        return graph

    @staticmethod
    def set_up_path_dict(stations):
        """Method to set up a path dictionary, which contains all stations as keys.
            :param stations: list of all stations
            :returns : a dictionary
        """
        path_dict = {}

        for s in stations:
            path_dict[s.id] = None

        return path_dict
